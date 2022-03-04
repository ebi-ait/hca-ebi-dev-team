import json
import time
import requests

TOKEN = 'replace with JWT token without BEARER'
SUBMISSION_URL = 'https://api.ingest.archive.data.humancellatlas.org/submissionEnvelopes/<replace_with_id>'


def get_submission_id(url: str):
    return url.split('/')[-1]


if __name__ == '__main__':
    headers = {
        'Content-type': 'application/json',
        'Authorization': f'Bearer {TOKEN}'
    }
    FILES_TO_REVALIDATE_FILENAME = f'{get_submission_id(SUBMISSION_URL)}_files_to_revalidate.json'
    with open(FILES_TO_REVALIDATE_FILENAME, 'r') as infile:
        files_to_revalidate = json.load(infile)

    for file in files_to_revalidate:
        url = file['_links']['invalid']['href']
        print(f'transition to invalid {url}')
        r = requests.put(url, headers=headers)
        r.raise_for_status()

    for file in files_to_revalidate:
        url = file['_links']['self']['href']
        print(f'patch validation job of {url}')
        patch = {"validationJob": None}

        r = requests.patch(url, json=patch, headers=headers)
        r.raise_for_status()

    time.sleep(5)

    for file in files_to_revalidate:
        url = file['_links']['invalid']['href']
        url = url.replace('invalid', 'draft')
        print(f'transition to draft {url}')
        r = requests.put(url, headers=headers)
        r.raise_for_status()

    print('completed!')
