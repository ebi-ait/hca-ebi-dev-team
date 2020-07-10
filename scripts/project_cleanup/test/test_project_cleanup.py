from unittest.case import TestCase
import os
from ingest.api.ingestapi import IngestApi
from scripts.project_cleanup.project_cleanup import ProjectCleanup


class TestProjectCleanup(TestCase):

    def test_cleanup(self):
        ingest_url = os.environ["INGEST_URL"]
        ingest_client = IngestApi(ingest_url)
        project_cleanup = ProjectCleanup(ingest_client)

        with open("keep.txt") as keep_file:
            projects_to_keep_uuids = [line.rstrip() for line in keep_file]
            project_cleanup.run(projects_to_keep_uuids)
