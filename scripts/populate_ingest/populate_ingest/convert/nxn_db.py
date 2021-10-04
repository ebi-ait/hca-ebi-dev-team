# --- core imports
from datetime import datetime
import logging
import pprint

# --- application imports
from ..constants import ACCESSION_PATTERNS
from ..convert.conversion_utils import get_accessions


class NxnDatabaseConverter:
    def __init__(self, ingest_schema, publication_service, publication_converter):
        self.ingest_schema = ingest_schema
        self.publication_service = publication_service
        self.publication_converter = publication_converter

    def convert(self, nxn_data):
        converted_projects = []
        for d in nxn_data.to_dict('records'):
            converted_projects.append(self.convert_row(d))

    def convert_row(self, nxn_data_row) -> dict:
        ingest_project = self.__create_ingest_project(nxn_data_row)

        # setting project title, project description, funders, contributors and publication and publicationsInfo
        publications, publication_info = self.__get_publication_info(nxn_data_row.get('DOI'))
        if publications:
            ingest_project['content'].update(publications)
        if publication_info:
            ingest_project['publicationsInfo'] = publication_info

        #  setting accessions
        # todo: fix issues with the nan in accessions
        # ingest_project['content'].update(get_accessions(nxn_data_row.get('Data location', ''), ACCESSION_PATTERNS))

        logging.debug(f'Converted nxn data row: {nxn_data_row} to \n'
                      f'ingest project: {pprint.pformat(ingest_project)}')
        return ingest_project

    def __create_ingest_project(self, nxn_data_row):
        ingest_project = {
            'content': {
                'schema_type': 'project',
                "describedBy": self.ingest_schema
            },
            'cellCount': nxn_data_row.get('Reported cells total', '').replace(",", ""),
            'identifyingOrganisms': [organism.strip() for organism in
                                     nxn_data_row.get('Organism').split(',')],
            'isInCatalogue': True,
            'wranglingNotes': f"Auto imported from nxn db {datetime.today().strftime('%Y-%m-%d')}"
        }

        # setting project short name
        ingest_project['content'].setdefault('project_core', {}).setdefault('project_short_name', 'tba')
        return ingest_project

    def __get_publication_info(self, doi: str):
        publication_info = self.publication_service.query_doi(doi)
        if publication_info:
            publications, info = self.publication_converter.convert(publication_info)
            return publications, info
        return None, None