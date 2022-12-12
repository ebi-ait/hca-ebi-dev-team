import argparse
import json
import logging
import math
import os
import requests as rq
from requests.exceptions import HTTPError

from hca_ingest.api.ingestapi import IngestApi

from config import Config
import tqdm

"""
The script follows the next steps to fix the missing size and fileContentType for DCP1 datasets:

1. Check the project UUID provided is valid 
2. Retrieve all data file metadata from azul
3. Parse and massage the data to avoid DCP/1 / HCA Release / DCP/2 analysis files (Not in ingest)
4. For each of the metadata files:
   a. Check metadata is not already filled (Priority: Ingest > Azul)
   b. PUT metadata file
"""

# TODO: Check if file metadata is editable (submission editable). Don't know how to do it without 1 API call/file


class NotPublishedUuidError(HTTPError):
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
        raise NotPublishedUuidError(r, uuid)
    return uuid


def define_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--project-uuid", type=is_published_uuid, required=True,
                        help="UUID of the project to be patched. Needs to be published in the DCP.")
    parser.add_argument("-d", "--dry-run", action="store_true", default=False, help="Dry-run flag. No PUT operations"
                                                                                    "will be performed.")

    return parser


def build_azul_query(project_uuid: str):
    """
    Build a ElasticSearch query to extract all metadata related to project with UUID "project_uuid", that does not
    have a workflow indicated. This is the best way to avoid getting DCP1 Analysis files.
    :param project_uuid:
    :return query:          string dump of query
    """
    query = {
        "projectId": {
            "is":
                [
                    project_uuid
                ]
        },
        "fileSource": {
            "is":
                [
                    None,
                    "Contributor",
                    "ArrayExpress",
                    "GEO",
                    "SCEA",
                    "SCP",
                    "LungMAP",
                    "Zenodo",
                    "Publication"
                ]
        }
    }
    return json.dumps(query)


def yield_pages(first_page, session):
    """
    There has to be a more elegant way to deal with pagination
    :param first_page:
    :param session:
    :return:
    """
    next_page = session.get(first_page['pagination']['next']).json()
    yield next_page
    while next_page['pagination'].get('next'):
        next_page = session.get(next_page['pagination']['next']).json()
        yield next_page


def get_files_metadata_from_azul(azul_base: str, query: str) -> list:
    """
    Retrieve file metadata from azul
    :param azul_base:       Base URL of Azul's API. Defaults to prod. From config.
    :param query:           Query in str format to pass as a filter
    :return files:          List of file metadata
    """
    # Build URL/endpoint and request metadata
    azul_manifest_request_endpoint = "index/files"
    session = rq.Session()

    # Get info from pagination with minimal load (1 entity)
    r = session.get(f"{azul_base}{azul_manifest_request_endpoint}?filters={query}&size=100")
    r.raise_for_status()
    r = r.json()

    hits = r['hits']
    for page in yield_pages(r, session):
        hits.extend(page['hits'])

    # Document ID (file metadata UUID) is outside of ["hits"]["files"], so some data massage
    def change_datafile_uuid(azul_hit: dict):
        azul_hit['files'][0]['uuid'] = azul_hit['entryId']
        return azul_hit
    files = list(map(change_datafile_uuid, hits))

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


def set_up_ingestapi(ingest_token: str, ingest_base_url: str) -> IngestApi:
    """
    Set up ingestApi object, with credentials to access and modify information in the database. URL is not asked because
    this script can only be run in production (Azul service not available in dev/staging)

    :param ingest_token:    Token to access/modify entities in ingest
    :param ingest_base_url: Ingest's API base URL. Defaults to prod
    :return ingest_api:     IngestApi object set up with token
    """
    ingest_api = IngestApi(ingest_base_url)
    ingest_api.set_token(f"Bearer {ingest_token}")
    return ingest_api


def patch_file_metadata(uuid_metadata_map: dict, ingest_api: IngestApi, dry_run: bool) -> [list, list]:
    """
    Send a PUT request to each of the files in the uuid_size_map with the updated size and fileContentType extracted
    from Azul
    :param uuid_metadata_map:   {file_uuid: metadata} map of all the files that need to be updated
    :param ingest_api:          IngestApi object with headers set up
    :param dry_run:             bool value, if True no PUT operations will be performed (But information will be logged)
    :return not_found:          List of file metadata that was not found in ingest
    :return already_filled:     List of file metadata that was already filled
    """
    not_found = []
    already_filled = []
    for uuid, metadata in tqdm.tqdm(uuid_metadata_map.items()):
        # Check file exists in Ingest (Non-organically described matrices are virtually indistinguishable via metadata)
        try:
            logging.info(f"Searching for file metadata for file {metadata['name']}")
            entity = ingest_api.get_entity_by_uuid('files', uuid)
        except HTTPError:
            not_found.append(metadata)
            continue

        # Check entity is not already filled in - Script will only fill size and fileContentType when both are missing
        if entity.get('size') and entity.get('fileContentType'):
            already_filled.append(metadata)
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

    return not_found, already_filled


def file_list_to_document(path: str, file_list: list):
    with open(path, 'w') as f:
        json.dump(file_list, f, indent=4, separators=(", ", ": "))


def main(project_uuid, dry_run):
    # Set up environment variables
    config = Config(os.environ)

    # Set-up logging & environment variables
    logging.basicConfig(filename=f'{project_uuid}.log', level=config.LOG_LEVEL, filemode='w',
                        format='%(levelname)s: %(message)s')
    print(f"A log of the operation will be saved in {project_uuid}.log")
    logging.info(f"Starting script for project {project_uuid}")
    if dry_run:
        logging.warning("Dry-run flag ON, no patch operations will be applied")

    # Query azul for the file metadata and massage the data a bit
    query = build_azul_query(project_uuid)
    azul_files_manifest = get_files_metadata_from_azul(config.AZUL_BASE, query)
    uuid_metadata_map = parse_azul_metadata(azul_files_manifest)

    # Create IngestApi object and set up credentials
    ingest_api = set_up_ingestapi(config.INGEST_TOKEN, config.INGEST_BASE)

    # Patch files (or log if dry-run is on)
    not_patched, already_filled = patch_file_metadata(uuid_metadata_map, ingest_api, dry_run)

    if not_patched:
        logging.warning("Some files were not found in ingest. Please find the list in 'not_patched.json'")
        file_list_to_document("not_patched.json", not_patched)

    if already_filled:
        logging.info("Some files were already filled. Please find the list in 'already_filled.json'")
        file_list_to_document("already_filled.json", already_filled)




if __name__ == "__main__":
    parser = define_parser()
    args = parser.parse_args()
    main(args.project_uuid, args.dry_run)