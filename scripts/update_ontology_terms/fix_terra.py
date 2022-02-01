import os
import utils
import logging

RESULTS_DIR = './results/'
UPDATED_PROJECTS_FILE = os.path.join(RESULTS_DIR, 'updated_projects.txt')
DCP1_UUIDS_FILE = './dcp1-project-uuids.txt'
GCP_BUCKET = 'gs://broad-dsp-monster-hca-prod-ebi-storage/prod'

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    for uuid in utils.read_lines(UPDATED_PROJECTS_FILE):
        try:
            if uuid not in [l.rstrip() for l in utils.read_lines(DCP1_UUIDS_FILE)]:
                logger.info(f'{uuid} not a DCP1 project, doing nothing.')
                continue
            
            logger.info(f'{uuid} is a DCP1 project')

            if not input('Would you like to continue with fixing the terra area for this project? (Y/n)').lower() == 'y':
                continue

            project = utils.get_project_by_uuid(uuid)
            submission = utils.get_submission_for_project(project)

            submission_state = submission.get_state().lower()

            if submission_state != 'exported':
                raise Exception(f'Submission must already be exported. State is {submission_state}')

            utils.run_command(f'gsutil -m rm -r {GCP_BUCKET}/{uuid}/metadata/sequence_file')
            utils.run_command(f'gsutil -m rm -r {GCP_BUCKET}/{uuid}/metadata/supplementary_file')
            utils.run_command(f'gsutil -m rm -r {GCP_BUCKET}/{uuid}/descriptors')
            utils.run_command(f'gsutil -m rm -r {GCP_BUCKET}/{uuid}/links')
            utils.run_command(f'gsutil -m rm -r {GCP_BUCKET}/{uuid}/data')
            
        except Exception as e:
            logger.error(f'Failed on project {uuid}')
            logger.error(e)
