import json
import requests

from scripts.retrigger_file_validation.trigger_file_validation import TOKEN
from scripts.retrigger_file_validation.trigger_file_validation import SUBMISSION_URL


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


def get_files_in_submission(submission_url, state):
    api_base = submission_url.split("/")[2]
    draft_url = f"https://{api_base}/files/search/findBySubmissionEnvelopeAndValidationState?envelopeUri={submission_url}&state={state}"
    files = get_all(draft_url, 'files')
    return list(files)


def generate_input_file(submission_url, filename):
    files_to_delete = get_files_in_submission(submission_url, 'VALIDATING')
    with open(filename, 'w') as outfile:
        print(f'Saving info on files to delete to {filename}')
        json.dump(files_to_delete, outfile, indent=4)


def get_submission_id(url: str):
    return url.split('/')[-1]


if __name__ == '__main__':
    headers = {
        'Content-type': 'application/json',
        'Authorization': f'Bearer {TOKEN}'
    }
    # 1. Get the list of file resources to be revalidated - save them in a file
    FILES_TO_REVALIDATE_FILENAME = f'{get_submission_id(SUBMISSION_URL)}_files_to_revalidate.json'
    generate_input_file(submission_url=SUBMISSION_URL, filename=FILES_TO_REVALIDATE_FILENAME)
