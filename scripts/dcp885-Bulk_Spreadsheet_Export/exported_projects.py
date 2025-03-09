import json
from urllib.parse import urljoin

import requests as requests
from hca_ingest.api.ingestapi import IngestApi


class ExportedProjects:
    def __init__(self, azul_url = 'https://service.azul.data.humancellatlas.org', api_url = 'https://api.ingest.archive.data.humancellatlas.org', token = ''):
        self.azul_url = azul_url
        self.api = IngestApi(api_url)
        if token:
            self.api.set_token(f'Bearer {token}')
        self.projects = {}
        self.submissions = {}
        self.project_submissions = {}

    def get_exported_projects(self):
        self.projects = {}
        for project_document in self.get_all_projects():
            project_uuid = self.get_document_uuid(project_document)
            if self.is_published_uuid(project_uuid):
                self.projects[project_uuid] = project_document
        return self.get_project_submissions(self.projects)

    def get_all_projects(self):
        projects_url = urljoin(self.api.url, 'projects')
        return self.api.get_all(projects_url, 'projects')

    def is_published_uuid(self, uuid: str) -> bool:
        azul_project_url = urljoin(self.azul_url, f'index/projects/{uuid}')
        r = requests.get(azul_project_url)
        return r.ok

    def get_project_submissions(self, all_projects: dict):
        self.submissions = {}
        self.project_submissions = {}

        for project_uuid, project in all_projects.items():
            submissions = self.get_submissions(project)
            if len(submissions) == 1:
                self.project_submissions[project_uuid] = self.convert_to_output(project, submissions[0])
        return self.project_submissions

    def get_submissions(self, project: dict):
        submissions_url = self.api.get_link_from_resource(project, 'submissionEnvelopes')
        return list(self.api.get_all(submissions_url, 'submissionEnvelopes'))

    def convert_to_output(self, project: dict, submission: dict):
        project_uuid = self.get_document_uuid(project)
        project_url = self.api.get_link_from_resource(project, 'self')
        submission_uuid = self.get_document_uuid(submission)
        submission_url = self.api.get_link_from_resource(submission, 'self')
        submission_state = submission.get('submissionState')
        self.submissions[submission_uuid] = submission
        return {
            'project_uuid': project_uuid,
            'project_url': project_url,
            'submission_uuid': submission_uuid,
            'submission_url': submission_url,
            'submission_state': submission_state
        }

    @staticmethod
    def get_document_uuid(document: dict) -> str:
        return document.get('uuid', {}).get('uuid')

    @staticmethod
    def save_json(filename: str, document: dict):
        with open(f'{filename}.json', 'w') as outfile:
            json.dump(document, outfile, indent=2)
