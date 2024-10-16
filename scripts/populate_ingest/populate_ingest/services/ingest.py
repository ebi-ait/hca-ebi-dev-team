import json
from collections import namedtuple
from enum import Enum
from typing import List

from ingest.api.ingestapi import IngestApi


class EntityType(Enum):
    FILES = 'files'
    PROCESSES = 'processes'
    BIOMATERIALS = 'biomaterials'
    PROJECTS = 'projects'
    PROTOCOLS = 'protocols'


Criteria = namedtuple('Criteria', ['field', 'operator', 'value'])

# ToDo: These methods should be added into the Ingest Client IngestApi class
class QuickIngest(IngestApi):
    def __init__(self, url=None, token_manager=None, token=None):
        super().__init__(url, token_manager)
        self.token = token

    def get_headers(self):
        if self.token_manager:
            return super().get_headers()
        if self.token and 'Authorization' not in self.headers:
            self.headers['Authorization'] = self.token
            self.logger.debug(f'Token set!')
        return self.headers

    def post(self, url, data):
        response = self.session.post(url, data=data, headers=self.get_headers())
        response.raise_for_status()
        return response.json()

    def new_project(self, project: dict):
        return self.create_entity(self.url, project, "projects")

    def query_entity(self, entity_type: EntityType, query: List[dict]):
        url = f'{self.url}/{entity_type.value}/query'
        data = json.dumps(query)
        response = self.post(url, data=data)
        return response

    def doi_exists(self, doi: str) -> bool:
        results = self.__project_doi_query(doi)
        count = results.get('page', {}).get('totalElements', 0)
        return count > 0

    def get_projects_by_doi(self, doi: str):
        results = self.__project_doi_query(doi)
        projects = results.get('_embedded', {}).get('projects', [])
        return projects

    def __project_doi_query(self, doi: str):
        query = []
        criteria = {
            'field': 'content.publications.doi',
            'operator': 'IS',
            'value': doi
        }
        query.append(criteria)
        return self.query_entity(EntityType.PROJECTS, query)

    def project_exists(self, uuid: str) -> bool:
        url = f'{self.url}/projects/search/findAllByUuid?uuid={uuid}'
        response = self.get(url)
        response.raise_for_status()
        results = response.json()
        count = results.get('page', {}).get('totalElements', 0)
        return count > 0

    def get_projects(self):
        return self.get_all(url=self.url + '/projects',entity_type='projects')
