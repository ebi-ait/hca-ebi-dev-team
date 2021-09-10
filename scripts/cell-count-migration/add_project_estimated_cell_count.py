import copy
import json
import logging
import time
from typing import List

import requests

INGEST_API = 'http://localhost:8080'
TOKEN = 'insert-token'

# This is the version which introduced cell count
TARGET_SCHEMA_URL = 'https://schema.humancellatlas.org/type/project/14.3.0/project'

DEFAULT_HEADERS = {'Content-type': 'application/json'}


def get_projects() -> List[dict]:
    response = requests.get(f'{INGEST_API}/projects/?size=1000', headers=DEFAULT_HEADERS)
    response.raise_for_status()
    body = response.json()
    projects = body['_embedded']['projects'] if '_embedded' in body else []
    return projects


def update_projects(projects: List[dict]):
    context = {
        'project_count': 0,
        'submission_envelope_count': 0,
        'cell_count_update_count': 0,
        'patch_by_project': {},
        'project_submission_envelopes': {},
        'patched_count': 0
    }

    try:
        for project in projects:
            update_project(context, project)
    except Exception as e:
        logging.exception(e)
        logging.error(f'An exception occurred {str(e)}. Saving context...')

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    write_json(context, f'add_project_estimated_cell_count-{timestamp}.json')


def update_project(context: dict, project: dict):
    project_uuid = project['uuid']['uuid']
    content = project.get('content', {})
    described_by = content.get('describedBy')

    if described_by != TARGET_SCHEMA_URL:
        context['project_count'] += 1
        patch = {
            'describedBy': TARGET_SCHEMA_URL
        }

        cell_count = project.get('cellCount')
        if cell_count and cell_count > 0:
            patch['estimated_cell_count'] = cell_count
            context['cell_count_update_count'] += 1

        project_url = project['_links']['self']['href']
        context['patch_by_project'][project_uuid] = {'patch': patch, 'patched': False}
        new_content = copy.deepcopy(content)
        new_content.update(patch)

        try:
            patch_project({'content': new_content}, project_url)
            context['patch_by_project'][project_uuid]['patched'] = True
            context['patched_count'] += 1
        except Exception as e:
            context['patch_by_project'][project_uuid]['error'] = str(e)

        submission_envelopes = get_project_submissions(project)
        if len(submission_envelopes) > 0:
            context['project_submission_envelopes'][project_uuid] = [extract_submission_data(submission) for submission
                                                                     in submission_envelopes]
            context['submission_envelope_count'] += 1
            submission_envelopes[0]


def patch_project(patch: dict, project_url: str):
    headers = {'Authorization': f'Bearer {TOKEN}', 'Content-type': 'application/json'}
    response = requests.patch(project_url, data=json.dumps(patch), headers=headers)
    response.raise_for_status()


def get_project_submissions(project: dict) -> List[dict]:
    submission_envelopes_url = project['_links']['submissionEnvelopes']['href']
    r = requests.get(submission_envelopes_url, headers=DEFAULT_HEADERS)
    result = r.json()
    submission_envelopes = result['_embedded']['submissionEnvelopes'] if '_embedded' in result else []
    return submission_envelopes


def extract_submission_data(submission: dict):
    return {
        'submission_uuid': submission['uuid']['uuid'],
        'submission_url': submission['_links']['self']['href'],
        'submission_state': submission['submissionState'],
        'createdDate': submission['submissionDate']
    }


def write_json(data: dict, filename: str):
    with open(filename, "w") as open_file:
        json.dump(data, open_file, indent=2)


if __name__ == '__main__':
    projects = get_projects()
    update_projects(projects)
