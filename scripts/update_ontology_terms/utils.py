import requests
import json
import os
from submission import Submission
import subprocess

INGEST_API_TOKEN = os.environ['INGEST_API_TOKEN']
INGEST_API = os.environ.get('INGEST_API_URL', 'https://api.ingest.archive.data.humancellatlas.org')
INGEST_API.strip('/')
DEFAULT_HEADERS = {'Content-type': 'application/json'}

def read_lines(file: str):
    with open(file, 'r') as f:
        for l in f:
            yield l.rstrip()
    
def get_protocol(protocol_uuid: str):
    r = requests.get(f'{INGEST_API}/protocols/search/findByUuid?uuid={protocol_uuid}')
    r.raise_for_status()
    return r.json()

def get_project_for_protocol(protocol: dict):
    r = requests.get(protocol['_links']['project']['href'])
    r.raise_for_status()
    return r.json()

def get_submission_for_protocol(protocol: dict):
    r = requests.get(protocol['_links']['submissionEnvelope']['href'])
    r.raise_for_status()
    return r.json()

def get_project_by_uuid(uuid: str):
    r = requests.get(f'{INGEST_API}/projects/search/findByUuid?uuid={uuid}')
    r.raise_for_status()
    return r.json()

def get_project_submissions(project: dict):
    submission_envelopes_url = project['_links']['submissionEnvelopes']['href']
    r = requests.get(submission_envelopes_url, headers=DEFAULT_HEADERS)
    result = r.json()
    submission_envelopes = result['_embedded']['submissionEnvelopes'] if '_embedded' in result else []
    return submission_envelopes

def patch(url: str, patch: dict):
    headers = {'Authorization': INGEST_API_TOKEN, 'Content-type': 'application/json'}
    r = requests.patch(url, data=json.dumps(patch), headers=headers)
    r.raise_for_status()
    return r.json()

def write_list_as_lines(file: str, lines):
    with open(file, 'w+') as f:
        f.writelines(list([f'{l}\n' for l in lines]))

def get_new_ontology_for_protocol(protocol):
    end_bias = protocol['content']['end_bias']
    ontology_text = protocol['content']['library_construction_method']['text']

    if end_bias == '3 prime tag':
        if 'v2' in ontology_text:
            return ('EFO:0009899', '10x 3\' v2')
        elif 'v3' in ontology_text:
            return ('EFO:0009922', '10x 3\' v3')
        else:
            raise Exception('Ontology is neither v2 or v3')
    elif end_bias == '5 prime tag':
        if 'v2' in ontology_text:
            return ('EFO:0009900', '10x 5\' v2')
        elif 'v3' in ontology_text:
            raise Exception('No ontology exists for 10x 5\' v3')
        else:
            raise Exception('Ontology is neither v2 or v3')
    else:
        raise Exception('End bias not accepted')

def get_submission_for_project(project):
    submissions = get_project_submissions(project)
    
    if(len(submissions) > 1):
        raise Exception(f'Project {project["uuid"]["uuid"]} has more than one submission')
    
    submission_url = submissions[0]['_links']['self']['href']

    return Submission(submission_url, INGEST_API_TOKEN)

def get_submission(uuid):
    r = requests.get(f'{INGEST_API}/submissionEnvelopes/search/findByUuidUuid?uuid={uuid}')
    r.raise_for_status()
    sub = r.json()

    return Submission(sub['_links']['self']['href'], INGEST_API_TOKEN)

def run_command(command: str):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    
    if error:
        raise Exception(f'Command failed: {error}')
    return output