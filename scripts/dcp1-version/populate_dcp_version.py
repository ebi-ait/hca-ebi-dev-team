import logging
import os
import uuid
from datetime import datetime

from bson import JAVA_LEGACY, CodecOptions
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

DCP1_GS_FILES_LS = os.environ.get('DCP1_GS_FILES_LS')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', 27017)

DB_CLIENT = MongoClient(DB_HOST, 27017)
DB = DB_CLIENT.get_database('admin')

DCP_VERSION_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

COLLECTION_MAP = {
    'project': 'project',
    'cell_line': 'biomaterial',
    'cell_suspension': 'biomaterial',
    'collection_protocol': 'protocol',
    'differentiation_protocol': 'protocol',
    'dissociation_protocol': 'protocol',
    'donor_organism': 'biomaterial',
    'enrichment_protocol': 'protocol',
    'ipsc_induction_protocol': 'protocol',
    'library_preparation_protocol': 'protocol',
    'organoid': 'biomaterial',
    'process': 'process',
    'sequence_file': 'file',
    'sequencing_protocol': 'protocol',
    'specimen_from_organism': 'biomaterial',
    'supplementary_file': 'file'
}


def load_lines_from_file(file: str):
    with open(file) as f:
        data = [line.rstrip() for line in f]
        return data


def find_type_uuid_version(line: str):
    filename = line.split('/')[-1]
    type = line.split('/')[-2]
    parts = filename.split('_')
    uuid_str = parts[0]
    version = parts[1].replace('.json', '')
    return type, uuid_str, version


def find_doc_by_uuid(collection: str, uuid_str: str):
    LOGGER.info(f'finding {uuid_str} in {collection}')
    # need to use java legacy uuid representation
    # https://stackoverflow.com/questions/26712600/mongo-uuid-python-vs-java-format/31061472
    db_collection = DB.get_collection(collection, CodecOptions(uuid_representation=JAVA_LEGACY))

    doc = db_collection.find_one(
        {
            'uuid.uuid': uuid.UUID(uuid_str),
            'isUpdate': False
        }
    )

    if not doc:
        LOGGER.error(f'No doc found for {uuid_str}')

    return doc


def determine_updates(doc: dict, date_obj: datetime):
    id = doc.get('_id')
    dcp_version = doc.get('dcpVersion')
    first_dcp_version = doc.get('firstDcpVersion')

    if dcp_version and first_dcp_version:
        LOGGER.info(
            f'{collection} {str(id)} already has firstDcpVersion {first_dcp_version} and dcpVersion {dcp_version}')
        return None

    update = {
        'firstDcpVersion': date_obj
    }
    if not doc.get('dcpVersion'):
        update['dcpVersion'] = date_obj

    return update


def update_dcp_versions(collection: str, doc: dict, date_obj: datetime):
    update = determine_updates(doc, date_obj)

    if update:
        DB[collection].update_one(
            {
                '_id': doc.get('_id')
            },
            {
                "$set": update
            }
        )
        LOGGER.info('updated!')


def convert_dcp_version_to_date(version: str):
    return datetime.strptime(version, DCP_VERSION_FORMAT)


if __name__ == '__main__':
    lines = load_lines_from_file(DCP1_GS_FILES_LS)
    for line in lines:
        concrete_entity_type, uuid_str, version = find_type_uuid_version(line)
        collection = COLLECTION_MAP[concrete_entity_type]
        doc = find_doc_by_uuid(collection, uuid_str)
        date_obj = convert_dcp_version_to_date(version)
        update_dcp_versions(collection, doc, date_obj)