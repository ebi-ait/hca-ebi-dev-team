import json
import sys
import requests
from multiprocessing.dummy import Pool

PROCESSES_COUNT = 5
DRY_RUN = False
OUTPUT_FILE = 'output.json'
INGEST_API = ''


def delete_submission(submission_id):
    print(f'Deleting {submission_id}')
    if not DRY_RUN:
        r = requests.delete(f'{INGEST_API}/submissionEnvelopes/{submission_id}?force=true')
        return r.status_code

    return f'Deleted {submission_id}!'


if __name__ == '__main__':
    input_file = sys.argv[1]

    with open(input_file, 'r') as f:
        submission_ids = json.load(f)

    output = []
    with Pool(PROCESSES_COUNT) as pool:
        output = pool.map(lambda submission_id: delete_submission(submission_id), submission_ids)
        pool.close()
        pool.join()

    with open(OUTPUT_FILE, 'w') as outfile:
        json.dump(output, outfile, indent=4)
