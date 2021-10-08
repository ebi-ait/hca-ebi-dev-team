# --- core imports
from datetime import datetime
import logging
import pprint

# --- application imports
from ..constants import ACCESSION_PATTERNS
from ..utils import get_accessions, not_is_nan


class NxnDatabaseConverter:
    def __init__(self, ingest_schema, publication_service, publication_converter):
        self.ingest_schema = ingest_schema
        self.publication_service = publication_service
        self.publication_converter = publication_converter

    def convert(self, nxn_data):
        converted_projects = map(lambda d: self.convert_row(d), nxn_data.to_dict('records'))
        return list(converted_projects)

    def convert_row(self, nxn_data_row) -> dict:
        ingest_project = self.__create_ingest_project(nxn_data_row)

        # setting project title, project description, funders, contributors and publication and publicationsInfo
        publications, publication_info = self.__get_publication_info(nxn_data_row.get('DOI'))
        if publications:
            ingest_project['content'].update(publications)
        if publication_info:
            ingest_project['publicationsInfo'] = publication_info

        # setting project short name
        ingest_project['content'].setdefault('project_core', {}).setdefault('project_short_name', 'tba')

        #  setting accessions
        accessions = nxn_data_row.get('Data location', '')
        if not_is_nan(accessions):
            ingest_project['content'].update(get_accessions(accessions, ACCESSION_PATTERNS))

        logging.debug(f'Converted nxn data row: {nxn_data_row} to \n'
                      f'ingest project: {pprint.pformat(ingest_project)}')
        return ingest_project

    def __create_ingest_project(self, nxn_data_row):
        ingest_project = {
            'content': {
                'schema_type': 'project',
                "describedBy": self.ingest_schema
            },
            'identifyingOrganisms': [organism.strip() for organism in
                                     nxn_data_row.get('Organism').split(',')],
            'isInCatalogue': False,
            'wranglingNotes': f"Auto imported from nxn db {datetime.today().strftime('%Y-%m-%d')}"
        }

        cell_count = nxn_data_row.get('Reported cells total', '')
        ingest_project['cellCount'] = cell_count.replace(",", "") if not_is_nan(cell_count) else ''

        return ingest_project

    def __get_publication_info(self, doi: str):
        publication_info = self.publication_service.query_doi(doi)
        if publication_info:
            publications, info = self.publication_converter.convert(publication_info)
            return publications, info
        return None, None
