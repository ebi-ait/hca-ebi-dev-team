import argparse
import logging

import requests

from ingest_query import IngestQuery


def __set_logging_level(log_level):
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % log_level)
    logging.basicConfig(level=numeric_level)


class DataFixer:
    MISSING_ORGAN_DATA_PATH = 'resources/missing_organ.tsv'
    MISSING_TECHNOLOGY_DATA_PATH = 'resources/missing_tech.tsv'
    HCA_ONTOLOGY_API_URL = 'https://ontology.archive.data.humancellatlas.org/api/select?q='

    def __init__(self):
        self.iq = IngestQuery()
        self.dts_projects = {
            'organ': self.iq.get_projects_from_dts_from_sheet(DataFixer.MISSING_ORGAN_DATA_PATH),
            'technology': self.iq.get_projects_from_dts_from_sheet(DataFixer.MISSING_TECHNOLOGY_DATA_PATH)
        }

    def update_projects(self, data_type):
        logging.info(f"Update for {data_type} started")
        update_count = 0
        if report_only:
            logging.info("Report only, no real update is happening")
        projects = self.dts_projects.get(data_type)
        for uuid, project in projects.items():
            project_update_url = self.iq.get_project_update_url_by_uuid(uuid)
            if project_update_url:
                ontology = project.get(f'{data_type} ontology term').replace('_', ':')
                ontology_label = self.__get_ontology_label_by_term(ontology)
                if ontology_label:
                    payload = {
                        data_type: {
                            'ontologies': [
                                {
                                    'text': ontology_label,
                                    'ontology': ontology,
                                    'ontology_label': ontology_label
                                }
                            ]
                        }
                    }

                    if not report_only:
                        self.iq.patch_project(project_update_url, payload)
                    else:
                        logging.info(f'[Simulate] Updating project (project url: {project_update_url}) with {payload}')
                    update_count += 1
                else:
                    logging.info(f'In project (uuid:{uuid} the ontology lookup: {ontology} failed.')
            else:
                logging.info(f'Project can not be found in ingest: {uuid}')
        logging.info("Update finished")
        logging.info(f'{update_count} project has been updated with new {data_type}')

    def __get_ontology_label_by_term(self, ontology):
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
        '--organ', action='store_true',
        help='Fix missing organs'
    )
    parser.add_argument(
        '--technology', action='store_true',
        help='Fix missing technologies'
    )
    parser.add_argument(
        '--simulate', action='store_true', help='Create report only'
    )
    args = parser.parse_args()
    __set_logging_level(args.log_level)

    report_only = args.simulate
    data_types = []
    if args.organ:
        data_types.append('organ')
    if args.technology:
        data_types.append('technology')

    fixer = DataFixer()
    for data_type in data_types:
        fixer.update_projects(data_type)
