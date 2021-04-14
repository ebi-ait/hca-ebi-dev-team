import argparse
import json
import re
from multiprocessing.dummy import Pool

from typing import IO, Any, Union, Dict
from io import StringIO, BufferedReader

from google.cloud import storage

from google.oauth2.service_account import Credentials

Streamable = Union[BufferedReader, StringIO, IO[Any]]

PROCESSES_COUNT = 30

# gsutil ls "gs://broad-dsp-monster-hca-prod-ebi-storage/prod/*/descriptors/*"  > descriptors.txt
DESCRIPTORS_FILE = 'descriptors.txt'
BUCKET_NAME = 'broad-dsp-monster-hca-prod-ebi-storage'
ENV_PREFIX = 'prod'


def dict_to_json_stream(d: Dict) -> StringIO:
    return StringIO(json.dumps(d))


def read_lines(filename):
    lines = []
    with open(filename) as f:
        lines = [line.strip() for line in f]
    return lines


class GoogleCloudStorage(object):
    def __init__(self, service_account_credentials_path):
        with open(service_account_credentials_path) as source:
            info = json.load(source)
            credentials: Credentials = Credentials.from_service_account_info(info)
            self.client = storage.Client(credentials=credentials)

    def write_json(self, path: str, d: Dict, metadata: Dict):
        json_stream = dict_to_json_stream(d)
        self.write_file(path, json_stream, metadata)

    def read_json(self, path: str) -> Dict:
        blob: storage.Blob = storage.Blob.from_string(path, client=self.client)
        json_data = json.loads(blob.download_as_bytes())
        return json_data

    def write_file(self, path: str, data: Streamable, metadata: Dict):
        blob: storage.Blob = storage.Blob.from_string(path, client=self.client)
        blob.metadata = metadata
        blob.upload_from_file(data)

    def rename_file(self, path:str, new_key: str):
        blob: storage.Blob = storage.Blob.from_string(path, client=self.client)
        new_blob = blob.bucket.rename_blob(blob, new_key)
        print(f'Blob {blob.name} has been renamed to {new_blob.name}')


"""
The prepending of uuid and version in data file filenames were removed in the exporter implementation for updates
The old projects exported before this new implementation needs to be migrated with the following logic:
1. rename data file filenames to use original filenames from file metadata
2. update filenames in the descriptors
"""


class DataFileMigrationProcessor:
    def __init__(self, gcs: GoogleCloudStorage):
        self.gcs = gcs

    def process_file(self, descriptor_path: str):
        descriptor = self.gcs.read_json(descriptor_path)
        metadata_path = descriptor_path.replace('descriptors', 'metadata')
        metadata = self.gcs.read_json(metadata_path)

        metadata_filename = metadata['file_core']['file_name']
        descriptor_filename = descriptor['file_name']
        project_uuid = self.get_project_uuid(descriptor_path)

        if descriptor_filename != metadata_filename:
            self.rename_data_file(descriptor_filename, metadata_filename, project_uuid)
            self.update_descriptor_filename(descriptor, descriptor_path, metadata_filename)
        else:
            print(f'ignoring {descriptor_path} with filename {descriptor["file_name"]}')

    def update_descriptor_filename(self, descriptor, descriptor_path, metadata_filename):
        descriptor['file_name'] = metadata_filename

        print(f'overwriting file {metadata_filename}')

        self.gcs.write_json(descriptor_path, descriptor, {"export_completed": True})

        print(f'overwritten file {metadata_filename}')

    def rename_data_file(self, descriptor_filename, metadata_filename, project_uuid):
        prefix = f'{ENV_PREFIX}/{project_uuid}/data'
        old_data_file_path = f'gs://{BUCKET_NAME}/{prefix}/{descriptor_filename}'
        new_data_file_path = f'gs://{BUCKET_NAME}/{prefix}/{metadata_filename}'

        print(f'renaming {old_data_file_path} to {new_data_file_path}')

        new_name = f'{prefix}/{metadata_filename}'
        self.gcs.rename_file(old_data_file_path, new_name)

        print(f'renamed {old_data_file_path} to {new_data_file_path}')

    def get_project_uuid(self, descriptor_path):
        match = re.search('gs://.*/.*/(.+?)/descriptors', descriptor_path)

        if match:
            project_uuid = match.group(1)
            return project_uuid


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('service_account_credentials_path', help='The file path of GCP Service Account credentials')

    args = parser.parse_args()

    gcs = GoogleCloudStorage(args.service_account_credentials_path)

    paths = read_lines(DESCRIPTORS_FILE)
    descriptors = (path for path in paths if '.json' in path)

    processor = DataFileMigrationProcessor(gcs)
    with Pool(PROCESSES_COUNT) as pool:
        output = pool.starmap(processor.process_file, zip(descriptors))
        pool.close()
        pool.join()

