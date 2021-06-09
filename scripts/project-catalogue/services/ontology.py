import requests
from urllib.parse import quote


KNOWN_DISCREPANCIES = {
    "10X v3 3'": 'EFO_0009922',
    "10X v2 3'": 'EFO_0009899'
}


class QuickOntology:
    def __init__(self, url: str = None):
        if not url:
            url = 'https://www.ebi.ac.uk/ols/api'
        self.url = url.rstrip('/')
        self.organ_not_found = []
        self.tech_not_found = []
        self.nearest = {}

    def get_organ(self, search: str):
        params = {
            'groupField': 'iri',
            'allChildrenOf': 'http://purl.obolibrary.org/obo/UBERON_0000465',
            'ontology': ['hcao', 'uberon']
        }
        organ = self.ontology_search(search, params)
        if organ:
            return organ
        if search not in self.organ_not_found:
            self.organ_not_found.append(search)
            print(f'No ontology found for organ: {search}')


    def get_technology(self, search: str):
        params = {
            'groupField': 'iri',
            'allChildrenOf': ['http://purl.obolibrary.org/obo/OBI_0000711', 'http://purl.obolibrary.org/obo/OBI_0001686'],
            'ontology': 'efo',
        }
        technology = self.ontology_search(search, params)
        if technology:
            return technology
        if search not in self.tech_not_found:
            self.tech_not_found.append(search)
            print(f'No ontology found for technology: {search}')       

    def ontology_search(self, search: str, params: dict):
        if search in KNOWN_DISCREPANCIES:
            search = KNOWN_DISCREPANCIES[search]
        exact_result = self.search_exact_ontology(search, params)
        if exact_result:
            return self.map_to_hca(exact_result)
        nearest_result = self.search_nearest_ontology(search, params)
        if nearest_result:
            return self.map_to_hca(nearest_result)

    def search_exact_ontology(self, search: str, params:dict):
        params['exact'] = True
        results = self.perform_lookup(search, params)
        index = self.index_of_matching_label(search, results)
        return results[index] if index > -1 else None

    def search_nearest_ontology(self, search, params):
        params['exact'] = False
        results = self.perform_lookup(search, params)
        if results:
            index = self.index_of_matching_label(search, results)
            if index > 1:
                return results[index]
            if search not in self.nearest:
                self.nearest[search] = results[0]
                print(f'No exact match for: {search}, so using: {results[0].get("label")}({results[0].get("obo_id")})')
            return results[0]

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
