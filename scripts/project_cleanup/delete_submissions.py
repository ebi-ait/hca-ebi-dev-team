import argparse
import json
import logging
import sys
import time

import requests
from ingest.api.ingestapi import IngestApi
from requests import HTTPError

if __name__ == '__main__':
    format = ' %(asctime)s  - %(name)s - %(levelname)s in %(filename)s:' \
             '%(lineno)s %(funcName)s(): %(message)s'
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=format)
    _LOGGER = logging.getLogger(__name__)
    logging.getLogger('ingest').setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser(
        description='Deletes submissions which were created before 2020 and not in the whitelist')
    parser.add_argument('filename', type=str, help='Submission uuids whitelist filename')
    parser.add_argument('env', choices=['dev', 'staging', 'prod'], help='environment')
    args = parser.parse_args()

    env = args.env
    infix = f'.{env}' if env != 'prod' else ''
    ingest_url = f'https://api.ingest{infix}.archive.data.humancellatlas.org'

    ingest_api = IngestApi(ingest_url)

    with open(args.filename, 'r') as file:
        data = file.read()

    whitelist = json.loads(data)

    summary = {}
    ctr = 0
    submission_envelopes = ingest_api.get_all(ingest_url + '/submissionEnvelopes', 'submissionEnvelopes')

    for submission in submission_envelopes:
        submission_uuid = submission['uuid']['uuid']
        try:
            url = submission['_links']['self']['href']
            created_date = submission['submissionDate']
            if created_date.startswith('2020'):  # don't delete recent submissions yet
                _LOGGER.warning(f'Skipping submission {submission_uuid} as it was created last {created_date}')
                continue
            if submission['isUpdate']:
                _LOGGER.warning(f'Skipping submission {submission_uuid} as it is an update submission')
            if submission_uuid not in whitelist:
                _LOGGER.info(f'Not in whitelist, deleting {submission_uuid} , {url}')
                ctr = ctr + 1
                r = requests.delete(url, params={'force': True})
                r.raise_for_status()
                _LOGGER.info(f'Deleted {submission_uuid}')
                time.sleep(1)

        except HTTPError as e:
            r = e.response
            if r.status_code == requests.codes.not_found:
                _LOGGER.warning(f'Submission {submission_uuid} is not found.')
            else:
                raise
    _LOGGER.info(f'Deleted {ctr} submissions')
