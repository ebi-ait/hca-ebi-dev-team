import requests


class Submission:
    def __init__(self, submission_url: str, token: str):
        self.submission_url = submission_url
        self.assay_process_count = 0
        self.biomaterial_count = 0
        self.process_count = 0
        self.headers = {'Content-type': 'application/json', 'Accept': 'application/hal+json'}
        self.auth_headers = {'Authorization': token, 'Content-type': 'application/json'}
        self.submission = None
        self.project = None

    def get_summary(self):
        if not self.submission:
            self.submission = self.get_submission()
        summary_url = self.submission['_links']['summary']['href']
        return self._get(summary_url)

    def get_uuid(self):
        if not self.submission:
            self.submission = self.get_submission()
        return self.submission['uuid']['uuid']

    def get_submission(self):
        return self._get(self.submission_url)

    def refresh(self):
        self.submission = self.get_submission()

    def get_state(self):
        if not self.submission:
            self.submission = self.get_submission()

        return self.submission.get('submissionState')

    def is_valid(self):
        # submission may be in Exported/Completed state
        # it's safer to verify that the validationState of all metadata is valid
        summary = self.get_summary()
        return summary.get('totalInvalid') == 0 and self.is_project_valid()

    def get_project(self):
        return self._get(f'{self.submission_url}/relatedProjects')['_embedded']['projects'][0]

    def is_project_valid(self):
        if not self.project:
            self.project = self.get_project()
        return self.project.get('validationState').lower() == 'valid'

    def set_to_valid(self):
        commit_valid_url = self.submission['_links']['commitValid']['href']
        self._put(commit_valid_url)

    def bypass_graph_validation(self):
        if not self.submission:
            self.submission = self.get_submission()

        links = self.submission['_links']

        self._put(links['commitGraphValidationRequested']['href'])
        self._put(links['commitGraphValidating']['href'])
        self._put(links['commitGraphValid']['href'])

    def submit(self):
        submit_url = self.submission['_links']['submit']['href']
        self._put(submit_url, ["Export_Metadata"])

    def _get(self, url: str):
        r = requests.get(url, headers=self.headers)
        r.raise_for_status()
        return r.json()

    def _put(self, url: str, data=None):
        if data:
            r = requests.put(url, json=data, headers=self.auth_headers)
        else:
            r = requests.put(url, headers=self.auth_headers)
        r.raise_for_status()
        return r.json()

    def _post(self, url: str, data: dict):
        r = requests.post(url, json=data, headers=self.auth_headers)
        r.raise_for_status()
        return r.json()
