import copy
import json
import logging
import time
from typing import List

import requests

INGEST_API = 'http://localhost:8080'
TOKEN = 'insert-token'
HCA_PUB_PROJECT_UUIDS_FILE = 'hca_pub_project_uuids.txt'

# This is the version which introduced cell count
TARGET_SCHEMA_URL = 'https://schema.humancellatlas.org/type/project/15.0.0/project'

DEFAULT_HEADERS = {'Content-type': 'application/json'}


def get_hca_pub_project_uuids():
    with open(HCA_PUB_PROJECT_UUIDS_FILE) as f:
        project_uuids = [line.rstrip() for line in f]
        return project_uuids


HCA_PUB_PROJECT_UUIDS = get_hca_pub_project_uuids()


def get_projects() -> List[dict]:
    response = requests.get(f'{INGEST_API}/projects?size=1000', headers=DEFAULT_HEADERS)
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
        logging.exception(e)
        logging.error(f'An exception occurred {str(e)}. Saving context...')

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    write_json(context, f'add_project_estimated_cell_count-{timestamp}.json')


def update_project(context: dict, project: dict):
    project_uuid = project['uuid']['uuid']
    content = project.get('content', {})
    described_by = content.get('describedBy')
    new_content = copy.deepcopy(content)

    if described_by != TARGET_SCHEMA_URL:
        context['project_count'] += 1

        new_content['describedBy'] = TARGET_SCHEMA_URL
        update_cell_count(context, project, new_content)
        update_official_hca_publication(context, new_content, project_uuid)

        project_url = project['_links']['self']['href']
        context['new_content_by_project'][project_uuid] = {'new_content': new_content, 'patched': False}

        try:
            patch_project({'content': new_content}, project_url)
            context['new_content_by_project'][project_uuid]['patched'] = True
            context['patched_count'] += 1
        except Exception as e:
            context['new_content_by_project'][project_uuid]['error'] = str(e)

        submission_envelopes = get_project_submissions(project)
        if len(submission_envelopes) > 0:
            context['project_submission_envelopes'][project_uuid] = [extract_submission_data(submission) for submission
                                                                     in submission_envelopes]
            context['submission_envelope_count'] += 1
            submission_envelopes[0]


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
