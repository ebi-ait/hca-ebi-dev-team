"""
Reads the report file of migration_to_project_15_0_0.py and trigger submissions for exporting

filename: PROD_add_project_estimated_cell_count-20210930-184927
file: https://drive.google.com/file/d/1qdG9ohjp3C5WWzTx0BO_u9WhE7OtSP4v/view?usp=sharing
folder location: https://drive.google.com/drive/u/2/folders/1eAya2x0z-q77gYXUg_Mw4GTg_PE46mBV
"""

import logging
import os
from datetime import datetime
from typing import List

import requests

from migration.submission import Submission
from migration.util import load_json, load_list, write_json

cwd = os.getcwd()
INGEST_API_TOKEN = os.environ['INGEST_API_TOKEN']
PROJECT_WHITELIST = load_list(cwd + '/migration/dcp1-project-uuids.txt')
INGEST_API = os.environ['INGEST_API_URL']
INGEST_API.strip('/')
DEFAULT_HEADERS = {'Content-type': 'application/json'}

# The submission will not be set back to Valid from Exported/Complete state if:
# 1. the project is updated and if the project is created first before the submission,
# the submission in Exported will not be set back to Valid
# 2. if any metadata is updated and the submission is in Complete state, it will not be set back to Valid

DO_FORCE_SET_VALID = False

# After state tracker pod is recreated, this can be set to True to submit and export only metadata via the API
DO_EXPORT = False


def get_project_submissions(project: dict) -> List[dict]:
    submission_envelopes_url = project['_links']['submissionEnvelopes']['href']
    r = requests.get(submission_envelopes_url, headers=DEFAULT_HEADERS)
    result = r.json()
    submission_envelopes = result['_embedded']['submissionEnvelopes'] if '_embedded' in result else []
    return submission_envelopes


def get_project_by_uuid(project_uuid: str):
    r = requests.get(f'{INGEST_API}/projects/search/findByUuid?uuid={project_uuid}')
    r.raise_for_status()
    return r.json()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    counts = {
        'already_valid': 0,
        'set_to_valid': 0,
        'do_not_set_to_valid': 0,
        'projects': 0,
        'exported': 0,
        'complete': 0
    }

    if DO_FORCE_SET_VALID:
        logger.warning("The state tracker pod should be deleted after force setting the submission"
                       " from Exported/Complete state to Valid")
        logger.warning("Recreating the pod should initialised the state tracker and sync its state")

    for project_uuid in PROJECT_WHITELIST:
        project = get_project_by_uuid(project_uuid)
        submissions = get_project_submissions(project)

        submissions = sorted(submissions, key=lambda s: datetime.strptime(s['submissionDate'], '%Y-%m-%dT%H:%M:%S.%fZ'))
        first_submission = submissions[0]
        submission_uuid = first_submission['uuid']['uuid']
        state = first_submission['submissionState']
        logger.info(f'project {project_uuid} submission {submission_uuid} state: {state}')

        submission_url = first_submission['_links']['self']['href']

        submission = Submission(submission_url, INGEST_API_TOKEN)
        submission_state = submission.get_state().lower()

        graph_validation_state = first_submission['graphValidationState']
        if graph_validation_state.lower() == 'pending':
            submission.bypass_graph_validation()
            logger.info(f'bypassed graph validation!')

        if submission_state in ['exported', 'complete']:
            if DO_FORCE_SET_VALID:
                if submission.is_valid():
                    logger.warning(f'project {project_uuid} submission {submission_url} should be set to valid')
                    try:
                        submission.set_to_valid()
                        logger.warning(f'project {project_uuid} submission {submission_url} has been set to valid')

                    except Exception as e:
                        logger.exception(e)
                        logger.warning(f'project {project_uuid} submission {submission_url} failed to be set to valid')
                else:

                    logger.warning(f'project {project_uuid} submission {submission_url} cannot NOT be set to valid')
            else:

                logger.warning(f'project {project_uuid} submission {submission_url} is {submission_state}')

        elif submission_state == 'valid':
            logger.warning(f'project {project_uuid} submission {submission_url} is already valid')

            if DO_EXPORT:
                logger.warning(f'submitting')
                try:
                    submission.submit()
                    logger.warning(f'submitted')
                except Exception as e:
                    logger.exception(e)
                    logger.warning(f'submission {submission_url} was not submitted')
        else:
            logger.warning(f'project {project_uuid} submission {submission_url} is {submission_state}')
