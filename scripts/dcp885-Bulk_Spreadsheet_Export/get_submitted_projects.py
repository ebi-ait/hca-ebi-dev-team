import json
import requests

from hca_ingest.api.ingestapi import IngestApi

api_url = 'https://api.ingest.archive.data.humancellatlas.org'
ingest_api = IngestApi(api_url)
token = '' # Your ingest token here
ingest_api.set_token(f'Bearer {token}')

def get_azul_projects():
    azul_projects = {}
    for project_document in get_all_projects():
        project_uuid = get_document_uuid(project_document)
        if is_published_uuid(project_uuid):
            azul_projects[project_uuid] = project_document
    return azul_projects

def get_all_projects():
    projects_url = f'{api_url}/projects'
    return ingest_api.get_all(projects_url, 'projects')

def get_document_uuid(document: dict) -> str:
    return document.get('uuid', {}).get('uuid')

def is_published_uuid(uuid: str) -> bool:
    azul_url = 'https://service.azul.data.humancellatlas.org'
    r = requests.get(f'{azul_url}/index/projects/{uuid}')
    return r.ok

def save_json(filename: str, document: dict):
    with open(f'{filename}.json', 'w') as outfile:
        json.dump(document, outfile, indent=2)

def get_all_submissions(all_projects: dict):
    single_submission_projects = {}
    multi_submission_projects = {}
    for project_uuid, project in all_projects.items():
        submissions = get_submissions(project)
        if len(submissions) != 1:
            multi_submission_projects[project_uuid] = len(submissions)
        else:
            single_submission_projects[project_uuid] = convert_to_output(project, submissions[0])
    return single_submission_projects, multi_submission_projects

def get_submissions(project: dict):
    submissions_url = ingest_api.get_link_from_resource(project, 'submissionEnvelopes')
    return list(ingest_api.get_all(submissions_url, 'submissionEnvelopes'))

def convert_to_output(project, submission):
    project_uuid = get_document_uuid(project)
    project_url = ingest_api.get_link_from_resource(project, 'self')
    submission_uuid = get_document_uuid(submission)
    submission_url = ingest_api.get_link_from_resource(submission, 'self')
    submission_state = submission.get('submissionState')
    return {
        'project_uuid': project_uuid,
        'project_url': project_url,
        'submission_uuid': submission_uuid,
        'submission_url': submission_url,
        'submission_state': submission_state
    }

projects = get_azul_projects()
save_json('azul_projects', projects)

single_projects, multi_projects = get_all_submissions(projects)
save_json('single_projects', single_projects)
save_json('multi_projects', multi_projects)
