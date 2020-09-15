import argparse
import os
from typing import List
import json
import subprocess
from typing import Dict
from dataclasses import dataclass

import boto3

FILE_IMAGE_LOCATION = 'docker://quay.io/ebi-ait/ingest-file-archiver'
FILE_ARCHIVER_VERSION = 'd2020-07-09.1'
AAP_URL = 'https://api.aai.ebi.ac.uk/auth'


@dataclass
class ArchiveJob:
    job_dict: Dict
    job_file_path: str
    job_stdout_path: str


class BatchFileArchiver:
    def __init__(self, aap_username: str, aap_password: str, aws_access_key: str, aws_key_secret: str, work_dir: str,
                 dry_run=False):
        self.aap_username = aap_username
        self.aap_password = aap_password
        self.aws_access_key = aws_access_key
        self.aws_key_secret = aws_key_secret
        self.work_dir = work_dir
        self.dry_run = dry_run

    def run(self, archive_jobs: Dict):
        split_jobs = self.split_archive_jobs(archive_jobs)
        for job in split_jobs:
            self.run_job(job)

    def run_job(self, archive_job: ArchiveJob):
        self.write_job_json(archive_job)
        job_bsub_command = self.bsub_command(archive_job)
        if self.dry_run:
            print(job_bsub_command)
        else:
            self.run_command(job_bsub_command, stdout_filename=archive_job.job_stdout_path)

    @staticmethod
    def run_command(cmd_string: str, stdout_filename: str):
        with open(stdout_filename, "w") as stdout_file:
            subprocess.Popen(cmd_string, shell=True, stdout=stdout_file)

    def split_archive_jobs(self, archive_jobs: Dict) -> List[ArchiveJob]:
        return [ArchiveJob({"jobs": [job]}, f'{self.work_dir}/job{i}.json', f'stdout_job{i}.txt') for (i, job) in
                enumerate(archive_jobs["jobs"])]

    @staticmethod
    def write_job_json(archive_job: ArchiveJob) -> str:
        with open(archive_job.job_file_path, "w") as job_dict_file:
            json.dump(archive_job.job_dict, job_dict_file, indent=4, separators=(',', ': '))
            return job_dict_file.name

    def bsub_command(self, archive_job: ArchiveJob) -> str:
        # job_memory = self.get_job_memory(archive_job)
        job_memory = 1000
        return f' bsub -M {str(job_memory)} "{self.singularity_command(archive_job)}'

    def get_job_memory(self, archive_job: ArchiveJob) -> int:
        if 'conversion' not in archive_job.job_dict["jobs"][0]:
            return 1000
        else:
            s3 = boto3.client('s3',
                              aws_access_key_id=self.aws_access_key,
                              aws_secret_access_key=self.aws_key_secret
                              )
            job_urls = [file_input['cloud_url'] for file_input in
                        archive_job.job_dict.get('jobs')[0]['conversion']['inputs']]
            file_sizes = [
                s3.head_object(Bucket=job_url.split('/')[2], Key="/".join(job_url.split('/')[3:]))['ContentLength']
                for job_url in job_urls]
            return int(max(file_sizes) / 1000 ** 2 + 10000)

    def singularity_command(self, archive_job: ArchiveJob) -> str:
        creds = f'-u={self.aap_username} -p={self.aap_password} -a={self.aws_access_key} -s={self.aws_key_secret}'
        return f'singularity run -B {self.work_dir}:/data {FILE_IMAGE_LOCATION}:{FILE_ARCHIVER_VERSION} -d=/data -f={archive_job.job_file_path} -l={AAP_URL} {creds}'


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run multiple file archiver bsub jobs in parallel')
    parser.add_argument('aap_username', type=str, help='AAP Username')
    parser.add_argument('aap_password', type=str, help='AAP Password')
    parser.add_argument('aws_access_key', type=str, help='AWS Access Key')
    parser.add_argument('aws_access_key_secret', type=str, help='AWS Access Key Secret')
    parser.add_argument('work_dir', type=str, help='Work directory to process the files')
    parser.add_argument('jobs_json_filepath', type=str, help='Jobs JSON File path')
    parser.add_argument('--dry_run', action='store_true', help='Dry run will only print the command')
    args = parser.parse_args()

    aap_username = args.aap_username
    aap_password = args.aap_password
    aws_access_key = args.aws_access_key
    aws_access_key_secret = args.aws_access_key_secret
    work_dir = args.work_dir
    jobs_json_filepath = args.jobs_json_filepath
    dry_run = args.dry_run

    os.makedirs(work_dir, exist_ok=True)

    with open(jobs_json_filepath, "r") as jobs_json_file:
        jobs_json_dict = json.load(jobs_json_file)
        batch_file_archiver = BatchFileArchiver(aap_username, aap_password, aws_access_key, aws_access_key_secret,
                                                work_dir, dry_run)
        batch_file_archiver.run(jobs_json_dict)
