import os
import json
from urllib.parse import urljoin

from exported_projects import ExportedProjects

FILE_NAME = 'graph_validation'

class ValidateAzulProjects(ExportedProjects):
    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
        self.filter_status = "Metadata valid"
        self.valid_projects = {}
        if os.path.isfile(f'{FILE_NAME}.json'):
            with open(f'{FILE_NAME}.json') as valid_projects_file:
                self.valid_projects = json.load(valid_projects_file)

    def validate_projects(self):
        if not self.valid_projects:
            self.valid_projects = self.get_valid_projects(self.get_exported_projects())
            self.save_json(FILE_NAME, self.valid_projects)
        for project in self.get_valid_projects(self.valid_projects).values():
            project[FILE_NAME] = "Requested" if self.send_graph_validation(project.get("submission_url")) else "Error"
            self.save_json(FILE_NAME, self.valid_projects)

    def get_valid_projects(self, projects: dict):
        valid_projects = {}
        for uuid, proj in projects.items():
            if proj.get("submission_state") == self.filter_status:
                valid_projects[uuid] = proj
        return valid_projects

    def send_graph_validation(self, submission_url: str) -> bool:
        url = urljoin(f'{submission_url}/', 'graphValidationRequestedEvent')
        response = self.api.put(url, json={})
        return response.ok
