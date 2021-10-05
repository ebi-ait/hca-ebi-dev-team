# --- core imports
import json
import unittest

# --- third party library imports
from pandas.testing import assert_frame_equal

# --- application imports
from populate_ingest.services.nxn_db import NxnDatabaseService
from populate_ingest.data_operations.compare_ingest_nxn_db import Compare
from populate_ingest.data_operations.filter_nxn_db import Filter
from populate_ingest.utils import get_ingest_data_contents

# test data for nxn db taken from
# https://docs.google.com/spreadsheets/d/1En7-UV0k0laDiIfjFkdn7dggyR7jIk3WH8QgXaMOZF0/edit#gid=0
class TestPopulateIngestFromNxnSetUp(unittest.TestCase):
    def setUp(self):
        # set up test nxn db data
        nxn_db_service_mock = NxnDatabaseService
        nxn_db_service_mock.url = 'tests/nxn_db.tsv'
        self.nxn_db_data_mock = nxn_db_service_mock.get_data()

        # set up test ingest data
        with open('tests/project_list.json') as f:
            self.ingest_data_mock = get_ingest_data_contents(json.load(f))


class TestCompareIngestNxnDb(TestPopulateIngestFromNxnSetUp):
    def test_compare_on_doi(self):
        actual = Compare.compare_on_doi(self.ingest_data_mock, self.nxn_db_data_mock)
        expected = self.nxn_db_data_mock.drop([0, 1])
        assert_frame_equal(actual, expected, check_dtype=False)

    def test_compare_on_accessions(self):
        actual = Compare.compare_on_accessions(self.ingest_data_mock, self.nxn_db_data_mock)
        expected = self.nxn_db_data_mock.drop([1])
        assert_frame_equal(actual, expected, check_dtype=False)

    def test_compare_on_title(self):
        actual = Compare.compare_on_title(self.ingest_data_mock, self.nxn_db_data_mock)
        expected = self.nxn_db_data_mock.drop([0, 1, 2])
        assert_frame_equal(actual, expected, check_dtype=False)


class TestFilterNxnDb(TestPopulateIngestFromNxnSetUp):
    def test_filter_by_organism(self):
        actual = Filter.filter_by_organism(self.nxn_db_data_mock)
        expected = self.nxn_db_data_mock.drop([1, 3, 4, 8])
        assert_frame_equal(actual, expected, check_dtype=False)

    def test_filter_by_technology(self):
        actual = Filter.filter_by_technology(self.nxn_db_data_mock)
        expected = self.nxn_db_data_mock.drop([3])
        assert_frame_equal(actual, expected, check_dtype=False)

    def test_filter_by_measurement(self):
        actual = Filter.filter_by_measurements(self.nxn_db_data_mock)
        expected = self.nxn_db_data_mock
        assert_frame_equal(actual, expected, check_dtype=False)


if __name__ == '__main__':
    unittest.main()
