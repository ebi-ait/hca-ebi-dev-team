import json
import sys

import requests

if len(sys.argv) < 3:
    print('Please pass file arguments metadata type and filename containing json')
    exit(1)

TYPE = sys.argv[1]
JSON_FILENAME = sys.argv[2]

VALID_TYPES = ['biomaterials', 'protocols', 'processes', 'files']
if TYPE not in VALID_TYPES:
    print(f'Invalid first argument for type, valid types are: {VALID_TYPES}')
    exit(1)

TOKEN = 'insert-jwt-token'
SUBMISSION_URL = 'insert-submission-url'

if not (TOKEN and SUBMISSION_URL):
    print('Please edit file to update TOKEN and SUBMISSION_URL VALUE')
    exit(1)

create_headers = {
    'Content-type': 'application/json',
    'Authorization': f'Bearer {TOKEN}'
}

with open(JSON_FILENAME, 'r') as infile:
    data = json.load(infile)
    metadata_json = {
        'content': data
    }

    r = requests.post(f'{SUBMISSION_URL}/{TYPE}', json=metadata_json, headers=create_headers)
    r.raise_for_status()
    new_protocol = r.json()

    r = requests.get(f'{SUBMISSION_URL}/relatedProjects')
    r.raise_for_status()
    projects = r.json()
    project_url = projects['_embedded']['projects'][0]['_links']['self']['href']

    link_headers = {
        'Content-type': 'text/uri-list',
        'Authorization': f'Bearer {TOKEN}'
    }

    metadata_project_url = new_protocol['_links']['project']['href']
    metadata_url = new_protocol['_links']['self']['href']
    metadata_projects_url = f'{metadata_url}/projects'

    requests.put(metadata_project_url, data=project_url, headers=link_headers)
    requests.post(metadata_projects_url, data=project_url, headers=link_headers)
