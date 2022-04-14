import argparse
import json
import time

import googleapiclient.discovery

from google.oauth2.service_account import Credentials

# GET transferOperations has quota of 500 requests per 100 secs
WAIT_TIME_INTERVAL_SEC = 60


class GCP:
    def __init__(self, service_account_credentials_path):
        with open(service_account_credentials_path) as source:
            info = json.load(source)
            credentials: Credentials = Credentials.from_service_account_info(info)
            self.client = googleapiclient.discovery.build('storagetransfer', 'v1', credentials=credentials,
                                                          cache_discovery=False)

    def get_operation(self, project_id, job_name):
        result = self.client.transferOperations().list(name="transferOperations",
                                                       filter=json.dumps({
                                                           "project_id": project_id,
                                                           "job_names": [job_name]
                                                       })).execute()
        print('Returned transferOperations: {}'.format(
            json.dumps(result, indent=4)))

        operations = result.get('operations', [])
        return operations[0] if len(operations) > 0 else None

    def is_job_done(self, project_id, job_name):
        operation = self.get_operation(project_id, job_name)

        return operation and operation.get('done', False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('service_account_credentials_path', help='The file path of GCP Service Account credentials')
    parser.add_argument('export_job_id', help='The export job id')

    args = parser.parse_args()

    project_id = 'mystical-slate-284720'

    dest_gs_bucket = 'broad-dsp-monster-hca-prod-ebi-storage'

    client = GCP(args.service_account_credentials_path)

    while not client.is_job_done(project_id, f'transferJobs/{args.export_job_id}'):
        print(f'waiting {WAIT_TIME_INTERVAL_SEC}s for job')
        time.sleep(WAIT_TIME_INTERVAL_SEC)

    print('job is done')
