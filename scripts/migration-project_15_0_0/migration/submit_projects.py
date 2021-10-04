"""
Reads the report file of migration_to_project_15_0_0.py and trigger submissions for exporting

filename: PROD_add_project_estimated_cell_count-20210930-184927
file: https://drive.google.com/file/d/1qdG9ohjp3C5WWzTx0BO_u9WhE7OtSP4v/view?usp=sharing
folder location: https://drive.google.com/drive/u/2/folders/1eAya2x0z-q77gYXUg_Mw4GTg_PE46mBV
"""

import logging
import os
from datetime import datetime

from migration.submission import Submission
from migration.util import load_json, load_list, write_json

cwd = os.getcwd()
REPORT_FILE = cwd + '/_local/PROD_add_project_estimated_cell_count-20210930-184927.json'
INGEST_API_TOKEN = os.environ['INGEST_API_TOKEN']
PROJECT_WHITELIST = load_list(cwd + '/migration/batch1.txt')
DO_EXPORT = False
DO_SET_VALID = False

if __name__ == '__main__':
    report = load_json(REPORT_FILE)
    submissions_by_project = report.get('project_submission_envelopes')
    logger = logging.getLogger(__name__)
    counts = {
        'already_valid': 0,
        'set_to_valid': 0,
        'do_not_set_to_valid': 0,
        'projects': 0,
        'exported': 0,
        'complete': 0
    }

    for project_uuid, submissions in submissions_by_project.items():
        if project_uuid not in PROJECT_WHITELIST:
            continue

        counts['projects'] += 1
        submissions = sorted(submissions, key=lambda s: datetime.strptime(s['createdDate'], '%Y-%m-%dT%H:%M:%S.%fZ'))
        first_submission = submissions[0]
        submission_url = first_submission['submission_url']
        submission = Submission(submission_url, INGEST_API_TOKEN)
        submission_state = submission.get_state().lower()
        if submission_state in ['exported', 'complete']:
            if DO_SET_VALID:
                if submission.is_valid():
                    logger.warning(f'project {project_uuid} submission {submission_url} should be set to valid')
                    try:
                        # submission.set_to_valid()
                        logger.warning(f'project {project_uuid} submission {submission_url} has been set to valid')
                        counts['set_to_valid'] += 1
                    except Exception as e:
                        logger.exception(e)
                        logger.warning(f'project {project_uuid} submission {submission_url} failed to be set to valid')
                else:
                    counts['do_not_set_to_valid'] += 1
                    logger.warning(f'project {project_uuid} submission {submission_url} cannot NOT be set to valid')
            else:
                counts[submission_state] += 1
                logger.warning(f'project {project_uuid} submission {submission_url} is {submission_state}')

        elif submission_state == 'valid':
            logger.warning(f'project {project_uuid} submission {submission_url} is already valid')
            counts['already_valid'] += 1

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

    write_json(counts, 'counts.txt')
