"""
This script was ran locally with modified version of ingest-core containing an endpoint to get an array assay process ids.
"""
import logging

import requests

from migration.submission import Submission
from migration.util import load_json, write_json

FILENAME = 'submission-envelopes.json'


class Submission2(Submission):
    def get_summary(self):
        submission_summary = {}
        for entity_type in ['biomaterials', 'protocols', 'processes', 'files']:
            submission_summary[entity_type] = self._get_entity_count(entity_type)

        submission_summary['assays'] = self._get_assay_count()
        return submission_summary

    def _get_entity_count(self, entity_type: str):
        if not self.submission:
            self.submission = self.get_submission()
        entities_url = self.submission['_links'][entity_type]['href']
        r = requests.get(entities_url, headers=self.headers)
        r.raise_for_status()
        count = r.json()['page']['totalElements']
        return count

    def _get_assay_count(self):
        if not self.submission:
            self.submission = self.get_submission()
        submission_url = self.submission['_links']['self']['href']
        assay_url = f'{submission_url}/assays'
        r = requests.get(assay_url, headers=self.headers)
        r.raise_for_status()
        assay_ids = r.json()
        return len(assay_ids)


if __name__ == '__main__':
    submissions_by_project = load_json(FILENAME)
    summary = {}
    for project_uuid, submissions in submissions_by_project.items():
        submission_url = submissions[0].get('submission_url')
        submission = Submission2(submission_url)
        try:
            summary[project_uuid] = submission.get_summary()
        except Exception as e:
            logging.exception(e)

    write_json(summary, 'summary.json')
