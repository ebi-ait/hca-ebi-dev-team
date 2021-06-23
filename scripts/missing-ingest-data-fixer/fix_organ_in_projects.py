import argparse
import logging

import requests

from ingest_query import IngestQuery


def __set_logging_level(log_level):
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % log_level)
    logging.basicConfig(level=numeric_level)


class OrganFixer:
    MISSING_ORGAN_DATA_PATH = 'resources/missing_organ.tsv'
    HCA_ONTOLOGY_API_URL = 'https://ontology.archive.data.humancellatlas.org/api/select?q='

    def __init__(self):
        self.iq = IngestQuery()
        self.dts_projects = self.iq.get_projects_from_dts_from_sheet(OrganFixer.MISSING_ORGAN_DATA_PATH)

    def update_projects(self):
        logging.info("Update started")
        for uuid, project in self.dts_projects.items():
            project_update_url = self.iq.get_project_update_url_by_uuid(uuid)
            if project_update_url:
                ontology = project.get('organ ontology term').replace('_', ':')
                organ_label = self.__get_organ_label_by_term(ontology)
                if organ_label:
                    payload = {
                        'organ': {
                            'ontologies': [
                                {
                                    'text': organ_label,
                                    'ontology': ontology,
                                    'ontology_label': organ_label
                                }
                            ]
                        }
                    }

                    if not report_only:
                        self.iq.patch_project(project_update_url, payload)
                else:
                    logging.info(f'In project (uuid:{uuid} the ontology lookup: {ontology} failed.')
            else:
                logging.info(f'Project can not be found in ingest: {uuid}')
        logging.info("Update finished")

    def __get_organ_label_by_term(self, ontology):
        response = requests.get(self.HCA_ONTOLOGY_API_URL + ontology).json()
        ontology_docs = response['response']['docs']
        ontology_count = len(ontology_docs)
        if ontology_count > 1 or ontology_count == 0:
            logging.info(f"This ontology: {ontology} has 0 or more than 1 label")
            return None

        label = ontology_docs[0]['label']

        return label


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Fix missing organs or technologies of ingest projects'
    )
    parser.add_argument(
        '--log_level', '-l', type=str, default='INFO',
        help='Override the default logging level: INFO',
        choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']
    )
    parser.add_argument(
        '--simulate', action='store_true', help='Create report only'
    )
    args = parser.parse_args()
    __set_logging_level(args.log_level)

    report_only = args.simulate = True

    fixer = OrganFixer()
    fixer.update_projects()
