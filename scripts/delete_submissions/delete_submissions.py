import argparse
import json
import os

from ingest.api.ingestapi import IngestApi
from ingest.utils.s2s_token_client import S2STokenClient, ServiceCredential
from ingest.utils.token_manager import TokenManager


INGEST_API = os.environ['INGEST_API']
GCP_FILE = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
JWT_AUDIENCE = os.environ['INGEST_API_JWT_AUDIENCE']


def delete_submission(ingest_api, submission_id, dry_run=False):
    print(f'Deleting {submission_id}')
    if not dry_run:
        r = ingest_client_api.session.delete(f'{INGEST_API}/submissionEnvelopes/{submission_id}?force=true',
                                             headers=get_headers(ingest_api))
        r.raise_for_status()
        return f'Deleted {submission_id}!'


def get_headers(ingest_api):
    return {
        "Authorization": f"Bearer {ingest_api.token_manager.get_token()}"
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Delete multiple submissions. This will not delete the project entity.')
    parser.add_argument('submission_ids_file', type=str, help='Input json file containing array of submission object ids.')
    parser.add_argument('--dry_run', action='store_true', help='Dry run will only print the command')
    args = parser.parse_args()

    submission_ids_file = args.submission_ids_file
    dry_run = args.dry_run

    with open(submission_ids_file, 'r') as f:
        submission_ids = json.load(f)

    credential = ServiceCredential.from_file(GCP_FILE)
    s2s_token_client = S2STokenClient(credential, JWT_AUDIENCE)
    token_manager = TokenManager(token_client=s2s_token_client)
    ingest_client_api = IngestApi(url=INGEST_API, token_manager=token_manager)

    for submission_id in submission_ids:
        delete_submission(ingest_client_api, submission_id, dry_run)
