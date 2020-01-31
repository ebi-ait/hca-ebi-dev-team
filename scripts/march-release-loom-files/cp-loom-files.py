from multiprocessing.dummy import Pool
import sys
import json
import subprocess
import os

tmp_folder = "tmp"


def download_list(json_data):
    files = []
    for p, fs in json_data.items():
        for f in fs:
            files.append((p,f))
    return files


def download(project, file):
    download_path = tmp_folder + "/" + project
    os.removedirs(download_path)
    os.makedirs(download_path)
    print(f'Downloading {project} {file}')
    subprocess.call(['wget', '-P', download_path, file])


def sync_s3_bucket(s3_dest):
    subprocess.call(f'aws s3 sync {tmp_folder} {s3_dest}'.split(" "))


if __name__ == '__main__':
    filename = sys.argv[1]
    s3_bucket = sys.argv[2]
    with open(filename, 'r') as datasets:
        data = json.load(datasets)
        ls = download_list(data)
        print(f'Download started')
        #with Pool(12) as p:
        #    p.map(lambda l: download(l[0], l[1]), ls)
        print(f'Download completed')
        print(f'Syncing started')
        sync_s3_bucket(s3_bucket)
        print(f'Syncing completed')
