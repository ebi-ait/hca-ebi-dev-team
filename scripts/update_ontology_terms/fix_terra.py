import os
import utils
import logging

RESULTS_DIR = './results/'
UPDATED_SUBMISSIONS_FILE = os.path.join(RESULTS_DIR, 'updated_submissions.txt')
SKIPPED_TERRA_FIXES_FILE = os.path.join(RESULTS_DIR, 'skipped_terra_fixes.csv') # project uuid, reason
DCP1_UUIDS_FILE = './dcp1-project-uuids.txt'
GCP_BUCKET = 'gs://broad-dsp-monster-hca-prod-ebi-storage/prod'

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    skipped = [] # (uuid, reason)[]

    for uuid in utils.read_lines(UPDATED_SUBMISSIONS_FILE):
        try:
            logger.info(f'Working on submission {uuid}')
            submission = utils.get_submission(uuid)
            submission_state = submission.get_state().lower()

            if submission_state != 'exported':
                raise Exception(f'Submission must already be exported. State is {submission_state}')

            project = submission.get_project()
            project_uuid = project['uuid']['uuid']

            logger.info(f'Found project {project_uuid}')

            if project_uuid not in [l.rstrip() for l in utils.read_lines(DCP1_UUIDS_FILE)]:
                logger.info(f'{project_uuid} not a DCP1 project, doing nothing.')
                skipped.append((uuid, f'Not DCP1. Project ID {project_uuid}'))
                continue
            
            logger.info(f'project {project_uuid} is a DCP1 project')

            # if not input('Would you like to continue with fixing the terra area for this submission? (Y/n)').lower() == 'y':
            #     skipped.append((uuid, 'Manually skipped'))
            #     continue

            utils.run_command(f'gsutil -m rm -r {GCP_BUCKET}/{project_uuid}/metadata/sequence_file')
            utils.run_command(f'gsutil -m rm -r {GCP_BUCKET}/{project_uuid}/metadata/supplementary_file')
            utils.run_command(f'gsutil -m rm -r {GCP_BUCKET}/{project_uuid}/descriptors')
            utils.run_command(f'gsutil -m rm -r {GCP_BUCKET}/{project_uuid}/links')
            utils.run_command(f'gsutil -m rm -r {GCP_BUCKET}/{project_uuid}/data')
            
        except Exception as e:
            logger.error(f'Failed on submission {uuid}')
            logger.error(e)
            skipped.append((uuid, f'Error {e}'))

    utils.write_list_as_lines(SKIPPED_TERRA_FIXES_FILE, [','.join(x) for x in skipped])
