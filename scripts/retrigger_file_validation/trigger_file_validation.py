import json
import time
import requests

TOKEN = 'replace with JWT token without BEARER'
SUBMISSION_URL = 'https://api.ingest.archive.data.humancellatlas.org/submissionEnvelopes/<replace_with_id>'
TERABYTE_IN_BYTES = 1024 * 1024 * 1024 * 1024


def get_submission_id(url: str):
    return url.split('/')[-1]


if __name__ == '__main__':
    headers = {
        'Content-type': 'application/json',
        'Authorization': f'Bearer {TOKEN}'
    }
    revalidate_files_file = f'{get_submission_id(SUBMISSION_URL)}_files_to_revalidate.json'
    with open(revalidate_files_file, 'r') as infile:
        files = json.load(infile)

    files_to_revalidate = []
    skipped_files = []
    batch_size = 0
    for file in files:
        new_batch_size = batch_size + file.get('size', TERABYTE_IN_BYTES)
        if (new_batch_size / TERABYTE_IN_BYTES) < 1:
            files_to_revalidate.append(file)
            batch_size = new_batch_size
        else:
            skipped_files.append(file)
            print(f'Skipping file: {file.get("fileName")} so as not to go over the 1TB limit')

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

    if skipped_files:
        print(f'Some files were skipped, keeping remaining files here: {revalidate_files_file}')
        with open(revalidate_files_file, 'w') as outfile:
            json.dump(skipped_files, outfile, indent=4)
        print(
            'Wait until AWS is processing this batch to and then re-run this script to trigger the remaining files.')

    print('completed!')
