import requests
from urllib.parse import quote

from submission_broker.submission.entity import Entity


KNOWN_DISCREPANCIES = {
    "10X v3 3'": "EFO_0009922",
    "10X v2 3'": "EFO_0009899",
    "nasal cavity mucosa ": "UBERON_0001826",
    "oral epithelium": "UBERON_0002424",
    "mucosa of oral region": "UBERON_0003343",
    "10X v1": "EFO_0009897",
    "ATAC-seq": "EFO_0010891",
    "vaculature": "UBERON_0007798",
    "tonsils": "UBERON_0002372",
    "haematopoetic system": "UBERON_0002390",
    "ATACSeq": "EFO_0007045",
    "BD Rhapsody": "EFO_0010964",
    "InDrops": "EFO_0008780",
    "scRRBS": "EFO_0008905",
    "scWGBS": "EFO_0008905",
    "Seqwell": "EFO_0008919",
    "SMARTer": "EFO_0010184",
    "SMARTer (C1)": "EFO_0010184",
    "SMARTer(C1)": "EFO_0010184",
    "pbmc": "UBERON_0000178",
    "PBMCs": "UBERON_0000178"
}


class QuickOntology:
    def __init__(self, url: str = None):
        if not url:
            url = 'https://www.ebi.ac.uk/ols/api'
        self.url = url.rstrip('/')

    def get_organ(self, search: str, project: Entity):
        params = {
            'groupField': 'iri',
            'allChildrenOf': 'http://purl.obolibrary.org/obo/UBERON_0000465',
            'ontology': ['hcao', 'uberon']
        }
        organ = self.ontology_search(search, params, project)
        if organ:
            return organ
        project.add_error('organ.ontologies', f'No exact ontology found for organ: {search}')

    def get_technology(self, search: str, project: Entity):
        params = {
            'groupField': 'iri',
            'allChildrenOf': ['http://purl.obolibrary.org/obo/OBI_0000711', 'http://purl.obolibrary.org/obo/OBI_0001686'],
            'ontology': 'efo',
        }
        technology = self.ontology_search(search, params, project)
        if technology:
            return technology
        project.add_error('technology.ontologies', f'No exact ontology found for technology: {search}')

    def ontology_search(self, search: str, params: dict, project: Entity):
        if search in KNOWN_DISCREPANCIES:
            search = KNOWN_DISCREPANCIES[search]
        exact_result = self.search_exact_ontology(search, params)
        if exact_result:
            return self.map_to_hca(exact_result)
        nearest_result = self.search_nearest_ontology(search, params, project)
        if nearest_result:
            return self.map_to_hca(nearest_result)

    def search_exact_ontology(self, search: str, params:dict):
        params['exact'] = True
        results = self.perform_lookup(search, params)
        index = self.index_of_matching_label(search, results)
        return results[index] if index > -1 else None

    def search_nearest_ontology(self, search: str, params: dict, project: Entity):
        params['exact'] = False
        results = self.perform_lookup(search, params)
        if results:
            index = self.index_of_matching_label(search, results)
            if index > 1:
                return results[index]

    def perform_lookup(self, term: str, params: dict):
        url = f'{self.url}/select'
        params['q'] = quote(term)
        response = requests.get(url=url, params=params)
        response.raise_for_status()
        return response.json().get('response', {}).get('docs', [])

    @staticmethod
    def index_of_matching_label(search: str, results: list) -> int:
        if len(results) == 1:
            return 0
        for index, result in enumerate(results):
            if result.get('label', '').lower() == search.lower():
                return index
        return -1

    @staticmethod
    def map_to_hca(ols_result: dict):
        return {
          'ontology': ols_result.get('obo_id'),
          'ontology_label': ols_result.get('label'),
          'text': ols_result.get('label')
        }
