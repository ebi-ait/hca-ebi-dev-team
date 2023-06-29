import dataclasses
import json
import logging
import os
import re
from dataclasses import dataclass, field

import requests as requests
import requests_cache

from jsonschema.validators import validate as validate_against_schema

from hca_ingest.api.ingestapi import IngestApi

from dotenv import load_dotenv

load_dotenv()

requests_cache.install_cache('ingest')


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

    # def __repr__(self):
    #     return dataclasses.asdict(self)

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
    json_schema = requests.get(project["content"]["describedBy"]).json()
    validate_against_schema(instance=project["content"], schema=json_schema)
    project_url = api.get_link_from_resource(project, 'self')
    api.patch(project_url, json=project)


def add_bionetwork(project, bionetwork):
    hca_bionetworks: list = project['content'].setdefault('hca_bionetworks', [])
    bionetwork_as_dict = dataclasses.asdict(bionetwork)
    if bionetwork_as_dict not in hca_bionetworks:
        hca_bionetworks.append(bionetwork_as_dict)


def upgrade_schema_to_17_1_0(project, project_uuid):
    project_content = project['content']
    project_schema = project_content['describedBy']
    project_schema_version:str = re.findall('/project/(.*?)/project', project_schema)[0]    # upgrade schema
    if project_schema_version == '17.1.0':
        project_content['describedBy'] = 'https://schema.staging.data.humancellatlas.org/type/project/17.1.0/project'
        logging.info(f'project schema version OK: {project_schema_version}')
    elif project_schema_version == '17.0.0':
        project_content['hca_bionetworks'] = []
        project_content['describedBy'] = project_schema_version.replace('17.0.0', '17.1.0')
    else:
        raise ValueError(f'need to upgrade schema for project {project_uuid}. version is {project_schema_version}')


def run():
    token = os.environ.get('INGEST_TOKEN')
    api = IngestApi()
    api.set_token(f'Bearer {token}')
    update_bionetwork_for_project('cddab57b-6868-4be4-806f-395ed9dd635a',
                                  HCABionetwork(name='Adipose',
                                                hca_tissue_atlas='Blood',
                                                hca_tissue_atlas_version='v1.0',
                                                atlas_project=False), api)


if __name__ == '__main__':
    run()
