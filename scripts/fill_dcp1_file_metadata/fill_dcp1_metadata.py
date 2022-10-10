import requests as rq
import argparse
import json
import logging

from requests.exceptions import HTTPError

from hca_ingest.api.ingestapi import IngestApi

"""
The script follows the next steps to fix the missing size and fileContentType for DCP1 datasets:

1. Check the project UUID provided is valid 
2. Retrieve all data file metadata from azul
3. Parse and massage the data to avoid DCP/1 / HCA Release / DCP/2 analysis files (Not in ingest)
4. For each of the metadata files:
   a. Check metadata is not already filled (Priority: Ingest > Azul)
   b. PUT metadata file
"""
INGEST_TOKEN = ""

# TODO: Check if file metadata is editable (submission editable). Don't know how to do it without 1 API call/file


class NotPublishedUuid(HTTPError):
    def __init__(self, response: rq.Response, uuid: str):
        super().__init__(f"UUID {uuid} not found in Azul: GET request errored with status code {response.status_code}")


def is_published_uuid(uuid: str) -> str:
    """
    Check if the UUID provided corresponds to a published Azul project
    :param uuid:    UUID of the project which contains the files
    :return uuid:
    """
    r = rq.get(f"https://service.azul.data.humancellatlas.org/index/projects/{uuid}")
    try:
        r.raise_for_status()
    except HTTPError:
        raise NotPublishedUuid(r, uuid)
    return uuid


def define_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--project-uuid", type=is_published_uuid, required=True,
                        help="UUID of the project to be patched. Needs to be published in the DCP.")
    parser.add_argument("-d", "--dry-run", action="store_true", default=False, help="Dry-run flag. No PATCH operations"
                                                                                    "will be performed.")

    return parser


def build_azul_query(project_uuid: str):
    """
    Build a ElasticSearch query to extract all metadata related to project with UUID "project_uuid"
    :param project_uuid:
    :return query:          string dump of query
    """
    query = {
        "projectId": {
            "is":
                [
                    project_uuid
                ]
        }
    }
    return json.dumps(query)


def get_files_metadata_from_azul(query: str) -> list:
    """
    Retrieve file metadata from azul
    :param query:           Query in str format to pass as a filter
    :return files:          List of file metadata
    """
    # Build URL/endpoint and request metadata
    azul_base = "https://service.azul.data.humancellatlas.org/"
    azul_manifest_request_endpoint = "index/files"
    r = rq.get(f"{azul_base}{azul_manifest_request_endpoint}?filters={query}&size=100")
    r.raise_for_status()
    r = r.json()

    # Document ID (file metadata UUID) is outside of ["hits"]["files"], so some data massage
    def change_datafile_uuid(azul_hit: dict):
        azul_hit['files'][0]['uuid'] = azul_hit['entryId']
        return azul_hit
    files = list(map(change_datafile_uuid, r['hits']))

    # A bit more data massage to return only the file metadata (Easier parsing for later)
    files = [hit['files'][0] for hit in files]

    return files


def parse_azul_metadata(azul_file_list: list) -> dict:
    """
    Parse the azul metadata about the files and return a map {uuid: metadata}, excluding DCP1/2 analysis files
    :param azul_file_list:          File list from azul, output from get_files_metadata_from_azul()
    :return file_metadata_by_uuid:  Dictionary in the format {file_uuid:file_metadata} for all files in azul_file_list
    """
    uuid_metadata_map = {file['uuid']: file for file in azul_file_list}

    filesource_invalid_values = ["HCA Release", "DCP/2 Analysis", "DCP/1 Matrix Service"]
    uuid_metadata_map_filtered = {uuid: metadata for uuid, metadata in uuid_metadata_map.items()
                                  if not any([source == metadata['fileSource'] for source in filesource_invalid_values])}

    return uuid_metadata_map_filtered


def set_up_ingestapi() -> IngestApi:
    """
    Set up ingestApi object, with credentials to access and modify information in the database. URL is not asked because
    this script can only be run in production (Azul service not available in dev/staging)
    :return ingest_api: IngestApi object set up with token
    """
    ingest_api = IngestApi("https://api.ingest.archive.data.humancellatlas.org")
    ingest_api.set_token(f"Bearer {INGEST_TOKEN}")
    return ingest_api


def patch_file_metadata(uuid_metadata_map: dict, ingest_api: IngestApi, dry_run: bool):
    """
    Send a PUT request to each of the files in the uuid_size_map with the updated size and fileContentType extracted
    from Azul
    :param uuid_metadata_map:   {file_uuid: metadata} map of all the files that need to be updated
    :param ingest_api:          IngestApi object with headers set up
    :param dry_run:             bool value, if True no PUT operations will be performed (But information will be logged)
    :return:
    """
    for uuid, metadata in uuid_metadata_map.items():
        # Check file exists in Ingest (Non-organically described matrices are virtually indistinguishable via metadata)
        try:
            logging.info(f"Searching for file metadata for file {metadata['name']}")
            entity = ingest_api.get_entity_by_uuid('files', uuid)
        except HTTPError:
            logging.warning(f"Could not find file {metadata['name']} in ingest, please make sure it's not a "
                            f"non-organically described matrix.More details:")
            logging.warning(json.dumps(metadata, indent=4, separators=(", ", ": ")))
            continue

        # Check entity is not already filled in - Script will only fill size and fileContentType when both are missing
        if entity.get('size') and entity.get('fileContentType'):
            logging.warning(f"File {entity.get('fileName')}, with UUID {uuid} already has size and fileContentType set")
            continue

        # Add size and fileContentType to metadata
        entity['size'] = metadata['size']
        data_type = f"{'application/gzip' if metadata['format'] == 'fastq.gz' else 'application/octet-stream'}; dcp-type=data"
        entity['fileContentType'] = data_type

        logging.info(f"PATCH file {entity.get('fileName')}, uuid {uuid}, with size {entity['size']} and dcp-type {entity['fileContentType']}")

        if dry_run:
            continue

        # PUT the metadata back with the newly introduced values
        ingest_api.put(entity['_links']['self']['href'], json=entity)
        logging.info(f"PATCHED file {entity.get('fileName')}, url: {entity['_links']['self']['href']}")


def main(project_uuid, dry_run):
    # Set-up logging + early messages/warnings
    logging.basicConfig(filename=f'{project_uuid}.log', level=logging.INFO, filemode='w',
                        format='%(levelname)s: %(message)s')
    print(f"A log of the operation will be saved in {project_uuid}.log")
    logging.info(f"Starting script for project {project_uuid}")
    if dry_run:
        logging.warning("Dry-run flag ON, no patch operations will be applied")

    # Query azul for the file metadata and massage the data a bit
    query = build_azul_query(project_uuid)
    azul_files_manifest = get_files_metadata_from_azul(query)
    uuid_metadata_map = parse_azul_metadata(azul_files_manifest)

    # Create IngestApi object and set up credentials
    ingest_api = set_up_ingestapi()

    # Patch files (or log if dry-run is on)
    patch_file_metadata(uuid_metadata_map, ingest_api, dry_run)




if __name__ == "__main__":
    parser = define_parser()
    args = parser.parse_args()
    main(args.project_uuid, args.dry_run)