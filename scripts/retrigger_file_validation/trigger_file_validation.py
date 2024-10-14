import json
import time
import requests

TERABYTE_IN_BYTES = 1024 * 1024 * 1024 * 1024
# Replace with JWT token without BEARER
TOKEN = "eyJraWQiOiJyc2ExIiwidHlwIjoiYXQrand0IiwiYWxnIjoiUlMyNTYifQ.eyJhdWQiOiJlMjA0MWMyZC05NDQ5LTQ0NjgtODU2ZS1lODQ3MTFjZWJkMjEiLCJzdWIiOiJmM2VlMTczMjYyYTk3NmQ0ODlkMGRkZWY3NTI1MzcxZTE4NmY4YmRkQGVsaXhpci1ldXJvcGUub3JnIiwiYWNyIjoiaHR0cHM6Ly9yZWZlZHMub3JnL3Byb2ZpbGUvc2ZhIiwic2NvcGUiOiJlbWFpbCBvcGVuaWQgcHJvZmlsZSIsImF1dGhfdGltZSI6MTcyODkxMTkzMSwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5lbGl4aXItY3plY2gub3JnL29pZGMvIiwiZXhwIjoxNzI4OTI2MzgwLCJpYXQiOjE3Mjg5MTE5ODAsImNsaWVudF9pZCI6ImUyMDQxYzJkLTk0NDktNDQ2OC04NTZlLWU4NDcxMWNlYmQyMSIsImp0aSI6ImZlYTlkODQxLWE0YzQtNDE4NC1iMDc2LTFlODYyNzA4MjM5ZCJ9.Sre2UPwNH7YNfQN9nr3734po8dJrp6HavRR6B8PCYBZ6BND_zFfBsz8EEZ4QaaF9UEAI_cEPW3kyjLyIS6gZq1gPvT1qXaQL-H5UVpWFI06TZm1DCJTSbrI9lcw0tPEUlBepDGIRxookIRJKCovgMWNgnL7EFNkuGAiuD3gRLsr6RuS3hNZggCc9zdYRgkJyRkYOC5xOROv1PXiGwa2xFenOmRmR-DKh5HVIw4vAUgGmOiu6JFTNt8NFdZxt1gFdWW1zQLMRJvw1BNUlOjx8eYPpp-XLjAKZXDix08dAGtTzKFeJQtyQ0_NXD-ZN6gU_7LZnQrmV0eF1Cih5E8V0eA"
SUBMISSION_URL = "https://api.ingest.archive.data.humancellatlas.org/submissionEnvelopes/6707d06ef7e68c76e8ffb706"


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
