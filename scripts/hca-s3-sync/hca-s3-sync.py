from multiprocessing.dummy import Pool
import sys
import json
import subprocess


def sync_bucket_dir(source_dir, destination_bucket):
    print(f'Syncing {source_dir} to bucket {destination_bucket}')
    cmd = f'aws s3 sync {source_dir} {destination_bucket}'
    p = subprocess.call(cmd.split(" "), shell=True)
    print(f'Completed syncing {source_dir} to bucket {destination_bucket}')
    return p


def sync(source_dirs, destination_bucket):
    with Pool(30) as p:
        p.map(lambda source_dir: sync_bucket_dir(source_dir, destination_bucket), source_dirs)
        return 0


if __name__ == '__main__':
    filename = sys.argv[1]
    destination_bucket = sys.argv[2]
    with open(filename, 'rb') as f:
        source_dirs = json.load(f)["source_dirs"]
        sync(source_dirs, destination_bucket)
