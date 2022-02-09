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

def write_list_as_lines(file: str, lines):
    with open(file, 'w+') as f:
        f.writelines(list([f'{l}\n' for l in lines]))

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