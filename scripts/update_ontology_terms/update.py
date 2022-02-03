import os
import logging
from copy import deepcopy
from utils import get_submission_for_project, get_submission_for_protocol, patch, get_submission, read_lines, get_new_ontology_for_protocol, get_protocol, get_project_for_protocol, get_project_by_uuid, write_list_as_lines

INGEST_API = os.environ.get('INGEST_API_URL', 'https://api.ingest.archive.data.humancellatlas.org')
INGEST_API.strip('/')
INGEST_API_TOKEN = os.environ['INGEST_API_TOKEN']
INPUT_FILE = os.environ.get('INPUT_FILE', 'protocols.txt')

RESULTS_DIR = './results/'
APPLIED_PROTOCOL_PATCHES_FILE = os.path.join(RESULTS_DIR, 'applied_protocols_patches.csv') # CSV of uuid, text, ontology, ontology_label
ERRORED_PROTOCOLS_FILE = os.path.join(RESULTS_DIR, 'errored_protocols.txt')
SKIPPED_PROTOCOLS_FILE = os.path.join(RESULTS_DIR, 'skipped_protocols.txt')
UPDATED_PROJECTS_FILE = os.path.join(RESULTS_DIR, 'updated_projects.txt')
UPDATED_SUBMISSIONS_FILE = os.path.join(RESULTS_DIR, 'updated_submissions.txt')
SUBMITTED_FILE = os.path.join(RESULTS_DIR, 'submitted.txt')
SKIPPED_SUBMISSIONS_FILE = os.path.join(RESULTS_DIR, 'skipped_submissions.txt')
ERRORED_SUBMISSIONS_FILE  = os.path.join(RESULTS_DIR, 'errored_submissions.txt')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_protocols():
    if not input('Would you like to update the protocols? (Y/n)').lower() == 'y':
        return

    logger.info("Updating ontology terms in protocols...")

    protocols_tracker = {
        "updated_projects": set(),
        "updated_submissions": set(),
        "skipped": [],
        "errored": [],
        "patches": []
    }

    for uuid in read_lines(INPUT_FILE):
        try:
            logger.info(f'Updating protocol {uuid}')
            protocol = get_protocol(uuid)

            ontology, ontology_label = get_new_ontology_for_protocol(protocol)
            text = protocol['content']['library_construction_method']['text']
            
            new_content = deepcopy(protocol["content"])

            new_ontology = {
                "text": text,
                "ontology": ontology,
                "ontology_label": ontology_label
            }

            logger.info(f'New library_contruction_method: {new_ontology}')
            new_content["library_construction_method"] = new_ontology

            if input('Would you like to continue with patching this protocol? (Y/n)').lower() == 'y':
                patch(
                    protocol['_links']['self']['href'], 
                    { "content": new_content }
                )
                protocols_tracker['patches'].append([uuid, text, ontology, ontology_label])
                protocols_tracker['updated_projects'].add(get_project_for_protocol(protocol)['uuid']['uuid'])
                protocols_tracker['updated_submissions'].add(get_submission_for_protocol(protocol)['uuid']['uuid'])
            else:
                protocols_tracker['skipped'].append(uuid)
        except Exception as e:
            logger.error(f'Error updating protocol {uuid}')
            logger.error(e)
            protocols_tracker['errored'].append(uuid)

    write_list_as_lines(UPDATED_PROJECTS_FILE, list(protocols_tracker['updated_projects']))
    write_list_as_lines(UPDATED_SUBMISSIONS_FILE, list(protocols_tracker['updated_submissions']))
    write_list_as_lines(ERRORED_PROTOCOLS_FILE, protocols_tracker['errored'])
    write_list_as_lines(APPLIED_PROTOCOL_PATCHES_FILE, [','.join(x) for x in protocols_tracker['patches']])
    write_list_as_lines(SKIPPED_PROTOCOLS_FILE, protocols_tracker['skipped'])

    logger.info(f'Updated projects total: { len(protocols_tracker["updated_projects"]) }')
    logger.info(f'Updated submissions total: { len(protocols_tracker["updated_submissions"]) }')
    logger.info(f'Updated protocols total: { len(protocols_tracker["patches"]) }')
    logger.info(f'Skipped total: { len(protocols_tracker["skipped"]) }')
    logger.info(f'Errored total: { len(protocols_tracker["errored"]) }')
    logger.info('See output files for more details')

def export_submissions():
    if not input(f'Would you like to continue with exporting the submissions in {UPDATED_SUBMISSIONS_FILE}? (Y/n)').lower() == 'y':
        return

    submission_tracker = {
        "ready_to_submit": [],
        "submitted": [],
        "skipped": [],
        "errored": [] 
    }

    for submission_uuid in read_lines(UPDATED_SUBMISSIONS_FILE):
        try:
            submission = get_submission(submission_uuid)

            logger.info(f'submission {submission_uuid} state: {submission.get_state()}')

            if submission.get_state().lower() != 'graph valid':
                if submission.get_state().lower() == 'metadata valid':
                    submission.bypass_graph_validation()
                    submission.refresh()
                    logger.info(f'bypassed graph validation!')
                else:
                    raise RuntimeError(f'Submission not metadata valid is {submission.get_state()}')
                
            submission_tracker['ready_to_submit'].append(submission)

        except Exception as e:
            submission_tracker['errored'].append(submission_uuid)
            logger.error(e)

    logger.warn('You must redeploy state tracker at this point')
    logger.info('You can use: kubectl rollout restart deployment ingest-state-tracking')
    if not input(f'Have you re-deployed state tracker? (Y/n)').lower() == 'y':
        return

    for submission in submission_tracker['ready_to_submit']:
        if submission.get_state().lower() != 'graph valid':
            raise RuntimeError('Submission state is not graph valid')

        if input(f'Are you sure you want to continue exporting submission {submission.get_uuid()}? (Y/n)').lower() == 'y':
            logger.info(f'Submitting {submission.get_uuid()}')
            submission.submit()
            logger.info(f'Submitted!')
            submission_tracker['submitted'].append(submission.get_uuid())
        else:
            submission_tracker['skipped'].append(submission.get_uuid())
    
    write_list_as_lines(SUBMITTED_FILE, submission_tracker['submitted'])
    write_list_as_lines(SKIPPED_SUBMISSIONS_FILE, submission_tracker['skipped'])
    write_list_as_lines(ERRORED_SUBMISSIONS_FILE, submission_tracker['errored'])

    logger.info(f'Submitted total: { len(submission_tracker["submitted"]) }')
    logger.info(f'Skipped total: { len(submission_tracker["skipped"]) }')
    logger.info(f'Errored total: { len(submission_tracker["errored"]) }')
    logger.info('See output files for more details')
    
if __name__ == '__main__':
    """
    Reads from INPUT_FILE, a list of protocols that need updating as per:
    https://app.zenhub.com/workspaces/operations-5fa2d8f2df78bb000f7fb2b5/issues/ebi-ait/hca-ebi-wrangler-central/334

    Patches the ontology terms as needed
    Triggers the exporting for each submissions
    Asks several questions at each point about whether to proceed
    """
    
    update_protocols()
    export_submissions()
    
