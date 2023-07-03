import dataclasses
import json
import logging
import os
import re
from dataclasses import dataclass, field
from urllib.parse import urlparse

import requests as requests
import requests_cache

from jsonschema.validators import validate as validate_against_schema

from hca_ingest.api.ingestapi import IngestApi

from dotenv import load_dotenv

load_dotenv()

requests_cache.install_cache(__name__)


@dataclass
class Project:
    content: dict = field(default_factory=lambda: dict())

    def with_schema_version(self, version: str):
        self.content['describedBy'] = f'https://schema.staging.data.humancellatlas.org/type/project/{version}/project'
        return self

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class HCABionetwork:
    name: str
    hca_tissue_atlas: str
    hca_tissue_atlas_version: str
    atlas_project: bool
    # TODO: wait until pattern regex is sorted see https://github.com/HumanCellAtlas/metadata-schema/pull/1526
    # describedBy: str = field(init=False, default_factory=lambda:'')
    schema_version: str = field(init=False, default_factory=lambda: '')

    def __str__(self):
        return json.dumps(self.__dict__)

    def __eq__(self, other):
        if isinstance(other, HCABionetwork):
            return self.__dict__ == other.__dict__
        elif isinstance(other, dict):
            return self.__dict__ == other
        else:
            raise ValueError(f'unsupported equality comparison with {type(other)}')


def update_bionetwork_for_project(project_uuid: str, bionetwork: HCABionetwork, api: IngestApi):
    project = api.get_project_by_uuid(project_uuid)
    upgrade_schema_to_17_1_0(project, project_uuid)
    add_bionetwork(project, bionetwork)
    # TODO: enable schema validation for the bionetwork document once https://github.com/HumanCellAtlas/metadata-schema/pull/1526 is done
    json_schema = requests.get(project["content"]["describedBy"]).json()
    validate_against_schema(instance=project["content"], schema=json_schema)
    project_url = api.get_link_from_resource(project, 'self')
    api.patch(project_url, json=project)
    logging.info(f'project {project_uuid} updated with network {bionetwork}')


def add_bionetwork(project, bionetwork: HCABionetwork):
    hca_bionetworks: list = project['content'].setdefault('hca_bionetworks', [])
    bionetwork_as_dict = dataclasses.asdict(bionetwork)
    bionetwork_as_dict['schema_version'] = '1.0.1'
    new_element = True
    for x in hca_bionetworks:
        if x['name'] == bionetwork.name:
            new_element = False
            x.update(bionetwork_as_dict)
    if new_element:
        hca_bionetworks.append(bionetwork_as_dict)


def upgrade_schema_to_17_1_0(project, project_uuid):
    project_content = project['content']
    project_schema = project_content['describedBy']
    project_schema_version: str = re.findall('/project/(.*?)/project', project_schema)[0]  # upgrade schema
    if project_schema_version == '17.1.1':
        logging.info(f'project schema version is OK: {project_schema_version}')
    elif project_schema_version == '17.1.0':
        logging.info(f'upgrading project schema version from {project_schema_version} to 17.1.1')
        project_content['describedBy'] = project_schema.replace('17.1.0', '17.1.1')
    elif project_schema_version == '17.0.0':
        logging.info(f'upgrading project schema version from {project_schema_version} to 17.1.1')
        project_content['hca_bionetworks'] = []
        project_content['describedBy'] = project_schema.replace('17.0.0', '17.1.1')
    else:
        # TODO: we might need to support additional upgrades. I will add
        #       support as needed whilst going over the different projects.
        raise ValueError(f'need to upgrade schema for project {project_uuid}. version is {project_schema_version}')


def run():
    token = os.environ.get('INGEST_TOKEN')
    api = IngestApi()
    api.set_token(f'Bearer {token}')
    # TODO: uuid param from command line
    project_uuids = [
        # copy uuids from spreadsheet
    ]
    for uuid in project_uuids:
        try:
            update_bionetwork_for_project(uuid,
                                          HCABionetwork(name='Kidney',
                                                        hca_tissue_atlas='Kidney',
                                                        hca_tissue_atlas_version='v1.0',
                                                        atlas_project=False),
                                          api)
        except Exception as e:
            logging.warning(f'problem with project {uuid}', exc_info=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(message)s')
    run()
