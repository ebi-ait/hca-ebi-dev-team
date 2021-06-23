import logging

import requests

from ingest_query import IngestQuery


class OrganFixer:
    MISSING_DATA_PATH = 'resources/missing_organ.tsv'
    HCA_ONTOLOGY_API_URL = 'https://ontology.archive.data.humancellatlas.org/api/select?q='

    def __init__(self):
        self.iq = IngestQuery()
        self.dts_projects = self.iq.get_projects_from_dts_from_sheet(OrganFixer.MISSING_DATA_PATH)

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

                    self.iq.patch_project(project_update_url, payload)
                else:
                    print(f'In project (uuid:{uuid} the ontology lookup failed.')
            else:
                print(f'Project can not be found in ingest: {uuid}')
        logging.info("Update finished")

    def __get_organ_label_by_term(self, ontology):
        response = requests.get(self.HCA_ONTOLOGY_API_URL + ontology).json()
        ontology_docs = response['response']['docs']
        ontology_count = len(ontology_docs)
        if ontology_count > 1 or ontology_count == 0:
            print(f"This ontology: {ontology} has 0 or more than 1 label")
            return None

        label = ontology_docs[0]['label']

        return label


if __name__ == '__main__':
    fixer = OrganFixer()
    fixer.update_projects()
