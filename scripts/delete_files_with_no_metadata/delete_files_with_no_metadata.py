import json
import time

import requests
import subprocess

DRY_RUN = False
TOKEN = 'insert-token-without-bearer-prefix'
SUBMISSION_URL = 'https://api.ingest.archive.data.humancellatlas.org/submissionEnvelopes/insert-submission-id'
SUBMISSION_UUID = 'insert-submission-uuid'
FILES_TO_DELETE_FILENAME = f'{SUBMISSION_UUID}_files_to_delete.json'


def run(command: str, input: str = None, verbose: bool = True):
    parsed_command = command.split(' ')
    proc = subprocess.Popen(parsed_command,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            )
    if input:
        stdout, stderr = proc.communicate(input.encode())
    else:
        stdout, stderr = proc.communicate()

    if verbose:
        print('$ ' + command)
        print(stdout.decode())
        print(stderr.decode())

    return proc.returncode, stdout.decode(), stderr.decode()


def remove_file(s3_file_path):
    if DRY_RUN:
        command = f'echo "Removing file {s3_file_path}"'
    else:
        command = f'aws s3 rm {s3_file_path} --profile embl-ebi'

    exit_code, output, error = run(command)

    if exit_code == 0:
        return f'Removed {s3_file_path}'
    else:
        return error


def get_all(url: str, entity_type: str):
    r = requests.get(url)
    r.raise_for_status()
    result = r.json()
    entities = result["_embedded"][entity_type] if '_embedded' in result else []
    yield from entities

    while "next" in result["_links"]:
        next_url = result["_links"]["next"]["href"]
        r = requests.get(next_url)
        r.raise_for_status()
        result = r.json()
        entities = result["_embedded"][entity_type]
        yield from entities


def get_draft_files_in_submission(submission_url):
    api_base = submission_url.split("/")[2]
    draft_url = f"https://{api_base}/files/search/findBySubmissionEnvelopeAndValidationState?envelopeUri={submission_url}&state=DRAFT&size=200"
    draft_files = get_all(draft_url, 'files')
    return list(draft_files)


def generate_input_file(submission_url, filename):
    files_to_delete = get_draft_files_in_submission(submission_url)
    with open(filename, 'w') as outfile:
        print(f'Saving info on files to delete to {filename}')
        json.dump(files_to_delete, outfile, indent=4)


if __name__ == '__main__':
    headers = {
        'Content-type': 'application/json',
        'Authorization': f'Bearer {TOKEN}'
    }
    # 1. Get the list of file resources to be deleted - save them in a file
    generate_input_file(submission_url=SUBMISSION_URL, filename=FILES_TO_DELETE_FILENAME)

    with open(FILES_TO_DELETE_FILENAME, 'r') as infile:
        files_to_delete = json.load(infile)

    # 2. Transition state to Validation then to Valid
    for file in files_to_delete:
        url = file['_links']['validating']['href']
        print(f'transition to validating {url}')
        r = requests.put(url, headers=headers)
        r.raise_for_status()

    time.sleep(5)

    for file in files_to_delete:
        url = file['_links']['validating']['href']
        url = url.replace('validating', 'valid')
        print(f'transition to valid {url}')
        r = requests.put(url, headers=headers)
        r.raise_for_status()

    time.sleep(5)

    # 3. Delete the files in s3
    for file in files_to_delete:
        cloud_url = file['cloudUrl']
        print(f'Removing file in s3 {cloud_url}')
        remove_file(cloud_url)

    time.sleep(5)

    # 4. Delete the files (already valid)
    for file in files_to_delete:
        url = file['_links']['self']['href']
        print(f'Deleting {url}')
        requests.delete(url, headers=headers)

    print('completed!')