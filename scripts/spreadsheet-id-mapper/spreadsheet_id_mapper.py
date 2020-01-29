from ingest.api.ingestapi import IngestApi

from typing import Dict, Iterable, Tuple
from itertools import chain
import sys
import json


def entity_id_path(entity_type: str) -> Tuple[str, str]:
    if entity_type.lower() == "biomaterial":
        return "biomaterial_core", "biomaterial_id"
    elif entity_type.lower() == "file":
        return "file_core", "file_name"
    elif entity_type.lower() == "process":
        return "process_core", "process_id"
    elif entity_type.lower() == "protocol":
        return "protocol_core", "protocol_id"
    elif entity_type.lower() == "project":
        return "project_core", "project_short_name"
    else:
        raise Exception(f'Unknown ingest entity type: {entity_type}')


def _uuid_entity_id_map(entities: Iterable[Dict]) -> Dict[str, Dict[str, str]]:
    entity_id_uuid_map = dict()

    for entity in entities:
        entity_schema_type = entity["content"]["describedBy"].split("/")[-1]
        entity_local_id_path = entity_id_path(entity["type"])
        entity_local_id = entity["content"][entity_local_id_path[0]][entity_local_id_path[1]]
        entity_uuid = entity["uuid"]["uuid"]

        if entity_schema_type not in entity_id_uuid_map:
            entity_id_uuid_map[entity_schema_type] = dict()
            entity_id_uuid_map[entity_schema_type][entity_uuid] = entity_local_id
        else:
            entity_id_uuid_map[entity_schema_type][entity_uuid] = entity_local_id

    return entity_id_uuid_map


def uuid_entity_id_map(submission_resource: Dict, ingest_api: IngestApi) -> Dict[str, Dict[str, str]]:
    """
    Given a submission resource, returns a mapping of spreadsheet IDs (e.g biomaterial_id, file_id) to ingest UUIDs.
    The mappings are partitioned by entity type, e.g speciment_from_organism, sequence_file

    e.g

    {
      "specimen_from_organism" : {
        "<uuid>" : "<spreadsheet_id>",
        ...
        ...
      },
      "sequence_file" : {
        "<uuid>" : "<spreadsheet_id>",
        ...
        ...
      },
      ...
      ...
    }

    :param ingest_api: an instance of the ingest-api client
    :param submission_resource: A submission resource represented as a JSON object/dict
    :return: a mapping of the local IDs in the submission (i.e spreadsheet IDs) to their corresponding UUIDs
    """
    biomaterials = ingest_api.get_related_entities("biomaterials", submission_resource, "biomaterials")
    files = ingest_api.get_related_entities("files", submission_resource, "files")
    processes = ingest_api.get_related_entities("processes", submission_resource, "processes")
    protocols = ingest_api.get_related_entities("protocols", submission_resource, "protocols")
    projects = ingest_api.get_related_entities("projects", submission_resource, "projects")

    return _uuid_entity_id_map(chain(biomaterials, files, processes, protocols, projects))


def main(ingest_api_url: str, submission_uuid: str):
    ingest_api = IngestApi(url=ingest_api_url)
    submission_resource = ingest_api.get_submission_by_uuid(submission_uuid)
    print(f'Generating mapping for submission at {submission_resource["_links"]["self"]["href"]}')
    mapping = uuid_entity_id_map(submission_resource, ingest_api)

    mapping_filename = f'mapping_{submission_uuid}.json'
    with open(mapping_filename, 'w') as f:
        print(f'Writing mapping JSON to {mapping_filename}')
        json.dump(mapping, f, indent=4, sort_keys=True)


if __name__ == "__main__":
    ingest_api_url = sys.argv[1]
    submission_uuids = sys.argv[2].split(",")

    for submission_uuid in submission_uuids:
        main(ingest_api_url, submission_uuid)
