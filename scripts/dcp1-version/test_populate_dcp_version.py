from datetime import datetime
from unittest import TestCase

from assertpy import assert_that
from populate_dcp_version import find_type_uuid_version, determine_updates


class PopulateDcpVersionTest(TestCase):
    def test_find_uuid_version(self):
        # given
        line = 'gs://broad-dsp-monster-hca-prod-ucsc-storage/prod/no-analysis/metadata/cell_line/06edf73c-a9ca-4a66-acf4-14495f2a1977_2019-05-15T13:54:25.988000Z.json'

        # when
        type, uuid, version = find_type_uuid_version(line)

        # then
        assert_that(type).is_equal_to('cell_line')
        assert_that(uuid).is_equal_to('06edf73c-a9ca-4a66-acf4-14495f2a1977')
        assert_that(version).is_equal_to('2019-05-15T13:54:25.988000Z')

    def test_determine_updates(self):
        # given
        doc = {
            '_id': 'id'
        }

        date_obj = datetime.now()
        # when
        updates = determine_updates(doc, date_obj)

        # then
        assert_that(updates).is_equal_to({'dcpVersion': date_obj, 'firstDcpVersion': date_obj})

    def test_determine_updates__only_first_dcp_version(self):
        # given
        another_date = datetime.now()
        doc = {
            '_id': 'id',
            'dcpVersion': another_date
        }

        date_obj = datetime.now()
        # when
        updates = determine_updates(doc, date_obj)

        # then
        assert_that(updates).is_equal_to({'firstDcpVersion': date_obj})