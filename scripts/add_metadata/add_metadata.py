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

TOKEN = 'eyJraWQiOiJyc2ExIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIzMDZjODc4OGZkNGU1MjRlMDY1MTYyMjkwYmU2NmQ5ZTlmMmRlM2Q3QGVsaXhpci1ldXJvcGUub3JnIiwiYXpwIjoiZTIwNDFjMmQtOTQ0OS00NDY4LTg1NmUtZTg0NzExY2ViZDIxIiwic2NvcGUiOiJlbWFpbCBvcGVuaWQgcHJvZmlsZSIsImlzcyI6Imh0dHBzOlwvXC9sb2dpbi5lbGl4aXItY3plY2gub3JnXC9vaWRjXC8iLCJleHAiOjE2NDYzOTg1OTYsImlhdCI6MTY0NjM4NDE5NiwianRpIjoiNjBmOGUyOTAtZmU4Yy00ZTBmLWFjN2UtNDJjMWM3ZWQzNjc2In0.oTVkJJuq7XTij0G-z3VC4nJyAvQkw35dmdWeqpGWb_JrYX2RwcAMSvZe49hVhMkgZKmNnPK_2XCU6RRNEbgntj7k7ZdRDPZmtJAeWf4_OMpso3l5SRs9y_elCYNymYzHpXQhwfICsYHNhzZKXCRX3aSnphZ1n5sCCjgHNgVbPx8QQmS1l91cmNuSzFCDuRFW_v3YQN18kaSuUrF0-UdErKfm031tZo7lpSzcGbNoX5Pz5dDGFC-q-gp60puBV0RBE32pIpLZbyaaJNpBP8P5r4dUw8WsFt2R5nq80jHr3aX_WBw_Fez2omwdFghTxFVknKj0rz9S722mEHfPk7txlA'
SUBMISSION_URL = 'https://api.ingest.dev.archive.data.humancellatlas.org/submissionEnvelopes/620b7a6536749124c9c235c0'

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
