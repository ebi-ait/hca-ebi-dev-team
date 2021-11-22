"""
This script iterates all projects from the ingest api and upgrade their metadata schema version to 15.0.0 .
This outputs a report file containing the updates done to the project and submissions info.
"""
import copy
import json
import logging
import os
import time
from typing import List

import requests

from migration.util import write_json, load_list

INGEST_API = os.environ['INGEST_API_URL']
INGEST_API.strip('/')
INGEST_API_TOKEN = os.environ['INGEST_API_TOKEN']

PROJECTS_FILE = os.environ.get('PROJECTS_FILE')

TARGET_SCHEMA_URL = 'https://schema.humancellatlas.org/type/project/15.0.0/project'

DEFAULT_HEADERS = {'Content-type': 'application/json'}

HCA_PUB_PROJECT_UUIDS = load_list('hca-pub-project-uuids.txt')

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def get_project_by_uuid(project_uuid: str):
    r = requests.get(f'{INGEST_API}/projects/search/findByUuid?uuid={project_uuid}')
    r.raise_for_status()
    return r.json()


def get_projects_from_uuids(projects: List[str]):
    return [get_project_by_uuid(project_uuid) for project_uuid in projects]


def get_projects() -> List[dict]:
    auth_headers = {'Authorization': f'Bearer {INGEST_API_TOKEN}', 'Content-type': 'application/json'}
    response = requests.get(f'{INGEST_API}/projects?size=1000', headers=auth_headers)
    response.raise_for_status()
    body = response.json()
    projects = body['_embedded']['projects'] if '_embedded' in body else []
    return projects


def update_projects(projects: List[dict]):
    context = {
        'project_count': 0,
        'submission_envelope_count': 0,
        'cell_count_update_count': 0,
        'new_content_by_project': {},
        'project_submission_envelopes': {},
        'patched_count': 0
    }

    try:
        for project in projects:
            update_project(context, project)
    except Exception as e:
        LOGGER.exception(e)
        LOGGER.error(f'An exception occurred {str(e)}. Saving context...')

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    write_json(context, f'add_project_estimated_cell_count-{timestamp}.json')


def update_project(context: dict, project: dict):
    project_uuid = project['uuid']['uuid']
    content = project.get('content', {})
    described_by = content.get('describedBy')
    new_content = copy.deepcopy(content)

    if described_by != TARGET_SCHEMA_URL:
        LOGGER.info(f'Processing project {project_uuid}...')
        context['project_count'] += 1

        new_content['describedBy'] = TARGET_SCHEMA_URL
        update_cell_count(context, project, new_content)
        update_official_hca_publication(context, new_content, project_uuid)

        project_url = project['_links']['self']['href']
        context['new_content_by_project'][project_uuid] = {
            'new_content': new_content,
            'patched': False,
        }

        try:
            response = patch_project({'content': new_content}, project_url)
            response.raise_for_status()
            context['new_content_by_project'][project_uuid]['patched'] = True
            context['patched_count'] += 1
            LOGGER.info(f'Updated project {project_uuid}...')
        except Exception as e:
            context['new_content_by_project'][project_uuid]['error'] = str(e)
            LOGGER.exception(f'Project {project_uuid} error: {str(e)}')


def update_official_hca_publication(context, new_content, project_uuid):
    publications = new_content.get('publications', [])
    if project_uuid in HCA_PUB_PROJECT_UUIDS:
        if len(publications) > 1:
            official_has_multi_pubs = context.get('official_has_multi_pubs', [])
            official_has_multi_pubs.append(project_uuid)
            context['official_has_no_pubs'] = official_has_multi_pubs
            for pub in publications:
                pub['official_hca_publication'] = True
        elif len(publications) == 0:
            official_has_no_pubs = context.get('official_has_no_pubs', [])
            official_has_no_pubs.append(project_uuid)
            context['official_has_no_pubs'] = official_has_no_pubs
        elif len(publications) == 1:
            publications[0]['official_hca_publication'] = True
    else:
        for pub in publications:
            pub['official_hca_publication'] = False


def update_cell_count(context, project, new_content):
    cell_count = project.get('cellCount')
    if cell_count and cell_count > 0:
        new_content['estimated_cell_count'] = cell_count
        context['cell_count_update_count'] += 1


def patch_project(patch: dict, project_url: str):
    headers = {'Authorization': f'Bearer {INGEST_API_TOKEN}', 'Content-type': 'application/json'}
    response = requests.patch(project_url, data=json.dumps(patch), headers=headers)
    return response


def get_project_submissions(project: dict) -> List[dict]:
    submission_envelopes_url = project['_links']['submissionEnvelopes']['href']
    r = requests.get(submission_envelopes_url, headers=DEFAULT_HEADERS)
    result = r.json()
    submission_envelopes = result['_embedded']['submissionEnvelopes'] if '_embedded' in result else []
    return submission_envelopes


if __name__ == '__main__':
    if PROJECTS_FILE:
        project_uuids = load_list(PROJECTS_FILE)
        projects = get_projects_from_uuids(project_uuids)
    else:
        projects = get_projects()
    update_projects(projects)
