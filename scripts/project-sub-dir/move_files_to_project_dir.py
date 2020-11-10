import json
import sys
from multiprocessing.dummy import Pool
import subprocess

PROCESSES_COUNT = 20
PARENT_DIR = 'gs://broad-dsp-monster-hca-prod-ebi-storage/prod'
NEW_PARENT_DIR = 'gs://broad-dsp-monster-hca-prod-ebi-storage/prod2'
DRY_RUN = True
OUTPUT_FILE = 'output.json'


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


def copy_file(file_path, new_file_path):
    if DRY_RUN:
        command = f'echo "Copying file {file_path} to {new_file_path}"'
    else:
        command = f'gsutil cp {file_path} {new_file_path}'

    exit_code, output, error = run(command)

    if exit_code == 0:
        return f'Moved {file_path} to {new_file_path}'
    else:
        return error


if __name__ == '__main__':
    files_by_project_file = sys.argv[1]

    with open(files_by_project_file, 'r') as f:
        files_by_project = json.load(f)

    all_file_paths = []
    all_new_file_paths = []
    for project_uuid, file_paths in files_by_project.items():
        for file_path in file_paths:
            new_file_path = file_path.replace(PARENT_DIR, f'{NEW_PARENT_DIR}/{project_uuid}')
            all_file_paths.append(file_path)
            all_new_file_paths.append(new_file_path)

    output = []
    with Pool(PROCESSES_COUNT) as pool:
        output = pool.starmap(copy_file, zip(all_file_paths, all_new_file_paths))
        pool.close()
        pool.join()

    with open(OUTPUT_FILE, 'w') as outfile:
        json.dump(output, outfile, indent=4)
