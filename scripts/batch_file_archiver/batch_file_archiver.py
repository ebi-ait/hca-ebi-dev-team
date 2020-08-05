from typing import List
import json
import sys
from multiprocessing.dummy import Pool
import subprocess
from typing import Dict
from dataclasses import dataclass


@dataclass
class ArchiveJob:
    job_dict: Dict
    job_file_path: str
    job_stdout_path: str


class BatchFileArchiver:

    def __init__(self, aap_username: str, aap_password: str, aws_access_key: str, aws_key_secret: str):
        self.aap_username = aap_username
        self.aap_password = aap_password
        self.aws_access_key = aws_access_key
        self.aws_key_secret = aws_key_secret

    def run(self, archive_jobs: Dict):
        split_jobs = self.split_archive_jobs(archive_jobs)
        Pool(len(split_jobs)).map(lambda job: self.run_job(job), split_jobs)

    def run_job(self, archive_job: ArchiveJob):
        self.write_job_json(archive_job)
        job_bsub_command = self.bsub_command(archive_job)
        self.run_command(job_bsub_command, stdout_filename=archive_job.job_stdout_path)

    @staticmethod
    def run_command(cmd_string: str, stdout_filename: str):
        with open(stdout_filename, "w") as stdout_file:
            subprocess.Popen(cmd_string, shell=True, stdout=stdout_file)

    @staticmethod
    def split_archive_jobs(archive_jobs: Dict) -> List[ArchiveJob]:
        return [ArchiveJob({"jobs": job}, f'job{i}.json', f'stdout_job{i}.txt') for (i, job) in enumerate(archive_jobs["jobs"])]

    @staticmethod
    def write_job_json(archive_job: ArchiveJob) -> str:
        with open(archive_job.job_file_path, "r") as job_dict_file:
            json.dump(archive_job.job_dict, job_dict_file)
            return job_dict_file.name

    def bsub_command(self, archive_job: ArchiveJob) -> str:
        return f' bsub -M 64000 "{self.singularity_command(archive_job)}"'

    def singularity_command(self, archive_job: ArchiveJob) -> str:
        creds = f'-u={self.aap_username} -p={self.aap_password} -a={self.aws_access_key} -s={self.aws_key_secret}'
        return f'singularity run -B /nfs/production/hca:/data docker://quay.io/ebi-ait/ingest-file-archiver:d2020-07-09.1 -d=/data -f=${archive_job.job_file_path} -l=https://api.aai.ebi.ac.uk/auth ${creds}"'


if __name__ == "__main__":
    aap_username = sys.argv[1]
    aap_password = sys.argv[2]
    aws_access_key = sys.argv[3]
    aws_access_key_secret = sys.argv[4]
    jobs_json_filepath = sys.argv[5]

    with open(jobs_json_filepath, "r") as jobs_json_file:
        jobs_json_dict = json.load(jobs_json_file)
        batch_file_archiver = BatchFileArchiver(aap_password, aap_password, aws_access_key, aws_access_key_secret)
        batch_file_archiver.run(jobs_json_dict)
