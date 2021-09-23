import json
import unittest
from unittest.mock import MagicMock, patch
from populate_ingest.populate_ingest_from_nxn import main

mock_ingest_api_url = "http://mockingestapi.com"
mock_token_path = "mock_token.txt"


class TestPopulateIngestFromNxn(unittest.TestCase):
        @patch('services.nxn_db.NxnDatabaseService')
        @patch('services.ingest.QuickIngest')
        def test(self, mock_ingest_api, mock_nxn_db):
                with open('nxn_db.tsv') as f:
                        mock_nxn_db.get_nxn_text = MagicMock(return_value=f.read())
                # mock_ingest_api.get_schemas = MagicMock()
                mock_ingest_api.new_project = MagicMock(return_value= {'uuid': {'uuid': 'created project'}})
                with open('project_list.json') as f:
                        mock_ingest_api.get_all = MagicMock(return_value=json.load(f))
                main(mock_token_path, True)

                assert mock_ingest_api.new_project.call_count == 5

if __name__ == '__main__':
        unittest.main()
