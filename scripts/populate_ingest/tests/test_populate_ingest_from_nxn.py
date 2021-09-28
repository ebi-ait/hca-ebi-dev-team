import json
import unittest
from unittest.mock import MagicMock, patch
from populate_ingest import populate_ingest_from_nxn
from assertpy import assert_that

# test data taken from
# https://docs.google.com/spreadsheets/d/1En7-UV0k0laDiIfjFkdn7dggyR7jIk3WH8QgXaMOZF0/edit#gid=0
class TestPopulateIngestFromNxn(unittest.TestCase):
        @patch('populate_ingest.populate_ingest_from_nxn.NxnDatabaseService.get_nxn_text')
        @patch('populate_ingest.populate_ingest_from_nxn.QuickIngest')
        def test_add_to_ingest_project_count(self, mock_ingest_api, mock_nxn_db):
                with open('tests/nxn_db.tsv') as f:
                        mock_nxn_db.return_value = f.read()
                mock_ingest_api.return_value.new_project = MagicMock(return_value={'uuid': {'uuid': 'created project'}})
                mock_ingest_api.return_value._get_ingest_links = MagicMock()
                with open('tests/project_list.json') as f:
                        mock_ingest_api.return_value.get_all = MagicMock(return_value=json.load(f))
                populate_ingest_from_nxn.main("tests/mock_token.txt", True)

                assert_that(mock_ingest_api.return_value.new_project.call_count).is_equal_to(4)


if __name__ == '__main__':
        unittest.main()
