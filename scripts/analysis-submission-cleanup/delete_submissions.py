import json
import sys

from multiprocessing.dummy import Pool

from ingest.api.ingestapi import IngestApi
from ingest.utils.s2s_token_client import S2STokenClient
from ingest.utils.token_manager import TokenManager

PROCESSES_COUNT = 12
DRY_RUN = False
OUTPUT_FILE = 'output.json'
INGEST_API = ''
GCP_FILE = ''


def delete_submission(ingest_api, submission_id):
    print(f'Deleting {submission_id}')
    if not DRY_RUN:
        r = ingest_client_api.session.delete(f'{INGEST_API}/submissionEnvelopes/{submission_id}?force=true',
                                             headers=get_headers(ingest_api))
        r.raise_for_status()
        return r.status_code

    return f'Deleted {submission_id}!'


def get_headers(ingest_api):
    return {
        "Authorization": f"Bearer {ingest_api.token_manager.get_token()}"
    }


if __name__ == '__main__':
    input_file = sys.argv[1]

    with open(input_file, 'r') as f:
        submission_ids = json.load(f)

    s2s_token_client = S2STokenClient()
    s2s_token_client.setup_from_file(GCP_FILE)
    token_manager = TokenManager(s2s_token_client)
    ingest_client_api = IngestApi(url=INGEST_API, token_manager=token_manager)

    output = []
    with Pool(PROCESSES_COUNT) as pool:
        output = pool.map(lambda submission_id: delete_submission(ingest_client_api, submission_id), submission_ids)
        pool.close()
        pool.join()

    with open(OUTPUT_FILE, 'w') as outfile:
        json.dump(output, outfile, indent=4)
