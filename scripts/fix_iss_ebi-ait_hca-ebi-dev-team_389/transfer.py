import argparse
import json
import subprocess
import time

import googleapiclient.discovery

from datetime import datetime
from google.oauth2.service_account import Credentials

# GET transferOperations has quota of 500 requests per 100 secs
WAIT_TIME_INTERVAL_SEC = 60


class GCP:
    def __init__(self, service_account_credentials_path, access_key_id, secret_access_key):
        with open(service_account_credentials_path) as source:
            info = json.load(source)
            credentials: Credentials = Credentials.from_service_account_info(info)
            self.client = googleapiclient.discovery.build('storagetransfer', 'v1', credentials=credentials,
                                                          cache_discovery=False)
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key

    def create_job(self, transfer_spec):
        result = self.client.transferJobs().create(body=transfer_spec).execute()
        print('Returned transferJob: {}'.format(
            json.dumps(result, indent=4)))
        return result

    def create_transfer_spec(self, description, project_id, source_s3_bucket, source_s3_path, source_s3_prefix,
                             dest_gs_bucket, dest_gs_path):
        start_date = datetime.now()

        transfer_job = {
            'description': description,
            'status': 'ENABLED',
            'projectId': project_id,
            'schedule': {
                'scheduleStartDate': {
                    'day': start_date.day,
                    'month': start_date.month,
                    'year': start_date.year
                },
                'scheduleEndDate': {
                    'day': start_date.day,
                    'month': start_date.month,
                    'year': start_date.year
                }
            },
            'transferSpec': {
                'awsS3DataSource': {
                    'bucketName': source_s3_bucket,
                    'path': source_s3_path,
                    'awsAccessKey': {
                        'accessKeyId': self.access_key_id,
                        'secretAccessKey': self.secret_access_key
                    }
                },
                'gcsDataSink': {
                    'bucketName': dest_gs_bucket,
                    'path': dest_gs_path
                },
                'objectConditions': {
                    'includePrefixes': [source_s3_prefix]
                }
            }

        }

        return transfer_job

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('service_account_credentials_path', help='The file path of GCP Service Account credentials')
    parser.add_argument('access_key_id', help='Your AWS access key id.')
    parser.add_argument(
        'secret_access_key',
        help='Your AWS secret access key.'
    )

    args = parser.parse_args()

    description = 'Fix issue: https://github.com/ebi-ait/hca-ebi-dev-team/issues/389'
    project_id = 'mystical-slate-284720'

    source_s3_bucket = 'org-hca-data-archive-upload-prod'
    source_s3_path = '3f3baa51-6577-41ce-b71c-18cf8917e459'
    source_s3_file = 'SRR8448146_1.fastq.gz'

    dest_gs_bucket = 'broad-dsp-monster-hca-prod-ebi-storage'
    dest_gs_path = '3f3baa51-6577-41ce-b71c-18cf8917e459'

    client = GCP(args.service_account_credentials_path, args.access_key_id, args.secret_access_key)
    transfer_spec = client.create_transfer_spec(description, project_id, source_s3_bucket, source_s3_path,
                                                source_s3_file, dest_gs_bucket, dest_gs_path)
    job = client.create_job(transfer_spec)
    job_name = job.get('name')

    while not client.is_job_done(project_id, job_name):
        print(f'waiting {WAIT_TIME_INTERVAL_SEC}s for job')
        time.sleep(WAIT_TIME_INTERVAL_SEC)

    print('job is done')

    source_gs_path = 'gs://broad-dsp-monster-hca-prod-ebi-storage/3f3baa51-6577-41ce-b71c-18cf8917e459/SRR8448146_1.fastq.gz'
    dest_gs_path = 'gs://broad-dsp-monster-hca-prod-ebi-storage/prod/559bb888-7829-41f2-ace5-2c05c7eb81e9/data/e40c9e4c-92a9-4a38-a85a-09fe3369f0f3_2020-12-14T11:35:30.864000Z_SRR8448146_1.fastq.gz'

    run(f'gsutil cp {source_gs_path} {dest_gs_path}', verbose=True)
