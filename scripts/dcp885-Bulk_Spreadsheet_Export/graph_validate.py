from urllib.parse import urljoin

from exported_projects import ExportedProjects

class ValidateAzulProjects(ExportedProjects):
    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
        self.filter_status = "Metadata valid"
        self.valid_projects = {}
        self.triggered = {}
        self.errored = {}

    def validate_projects(self):
        projects = self.get_exported_projects()
        for project in self.get_valid_projects(projects).values():
            project["graph_validation"] = "Requested" if self.send_graph_validation(project.get("submission_url")) else "Error"
            self.save_json('graph_validation', self.valid_projects)

    def get_valid_projects(self, projects: dict):
        self.valid_projects = {}
        for uuid, proj in projects.items():
            if proj.get("submission_state") == self.filter_status:
                self.valid_projects[uuid] = proj
        self.save_json('graph_validation', self.valid_projects)
        return self.valid_projects

    def send_graph_validation(self, submission_url: str) -> bool:
        url = urljoin(submission_url, 'graphValidationRequestedEvent')
        response = self.api.put(url)
        return response.ok
