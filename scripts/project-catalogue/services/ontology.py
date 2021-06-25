import requests
from urllib.parse import quote

from submission_broker.submission.entity import Entity

KNOWN_DISCREPANCIES = {
    "10x": "EFO_0008995",
    "10X": "EFO_0008995",
    "10X v1": "EFO_0009897",
    "10X v1 3'": "EFO_0009901",
    "10X v2 3'": "EFO_0009899",
    "10X v2 5'": "EFO_0009900",
    "10X v2 VDJ": "EFO_0010713",
    "10X v3 3'": "EFO_0009922",
    "10x VDJ": "EFO_0010713",
    "10X VDJ TCR": "EFO_0010714",
    "Adipose": "UBERON_0001013",
    "airway": "UBERON_0000065",
    "ATAC-seq": "EFO_0010891",
    "ATACSeq": "EFO_0007045",
    "BD Rhapsody": "EFO_0010964",
    "bladder": "UBERON_0001255",
    "Blood and other immune organs": "UBERON_0002193",
    "bone": "UBERON_0002481",
    "Bone marrow": "UBERON_0002371",
    "bone marrow": "UBERON_0002371",
    "Brain tumour": "UBERON_0000955",
    "Breast cancer": "UBERON_0001911",
    "colon/tumour": "UBERON_0001155",
    "Culture (lymphoblastoid cell line)": "NULL",
    "DART-seq": "EFO_0008706",
    "fetal liver": "UBERON_0002107",
    "fetal pituitary": "UBERON_0000007",
    "Gut": "UBERON_0001555",
    "gut": "UBERON_0001555",
    "haematopoetic system": "UBERON_0002390",
    "InDrops": "EFO_0008780",
    "Lung tumor xenograft": "UBERON_0002048",
    "mouse organoid and t cells": "NULL",
    "Mucosal tissue": "UBERON_0000344",
    "muscle": "UBERON_0002385",
    "Muta-seq": "NULL",
    "nasal": "UBERON_0001707",
    "nasal cavity": "UBERON_0001707",
    "nasal scraping": "UBERON_0001826",
    "nasal swab": "UBERON_0001707",
    "oral mucosa": "UBERON_0002424",
    "oral scraping": "UBERON_0002424",
    "Patch-seq": "EFO_0008853",
    "pbmc": "UBERON_0000178",
    "PBMCs": "UBERON_0000178",
    "plate scATAC-seq": "EFO_0010891",
    "respiratory and gastrointestinal tract": "UBERON_0000065,UBERON_0001555",
    "Salivary gland": "UBERON_0001044",
    "sci-ATAC-seq": "EFO_0010891",
    "sci-ATAC-seq3": "EFO_0010891",
    "sci-RNA-seq3": "EFO_0010550",
    "scRRBS": "EFO_0008905",
    "scWGBS": "EFO_0008905",
    "Seqwell": "EFO_0008919",
    "Skin": "UBERON_0002097",
    "skin": "UBERON_0002097",
    "SMARTer": "EFO_0010184",
    "SMARTer (C1)": "EFO_0010184",
    "SMARTer(C1)": "EFO_0010184",
    "SORT-seq": "NULL",
    "Sperm": "CL_0000019",
    "Synovial tissue": "UBERON_0007616",
    "tonsils": "UBERON_0002372",
    "tumour/skin": "UBERON_0002097",
    "umbilical cord blood": "UBERON_0012168",
    "vaculature": "UBERON_0007798",
    "mucosa of oral region": "UBERON_0003343",
    "nasal cavity mucosa ": "UBERON_0001826",
    "oral epithelium": "UBERON_0002424"
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
        organ = self.ontology_search(search, params)
        if organ:
            return organ
        project.add_error('organ.ontologies', f'No exact ontology found for organ: {search}')

    def get_technology(self, search: str, project: Entity):
        params = {
            'groupField': 'iri',
            'allChildrenOf': ['http://purl.obolibrary.org/obo/OBI_0000711',
                              'http://purl.obolibrary.org/obo/OBI_0001686'],
            'ontology': 'efo',
        }
        technology = self.ontology_search(search, params)
        if technology:
            return technology
        project.add_error('technology.ontologies', f'No exact ontology found for technology: {search}')

    def ontology_search(self, search: str, params: dict):
        if search in KNOWN_DISCREPANCIES:
            search = KNOWN_DISCREPANCIES[search]
        exact_result = self.match_ontology(search, params, exact=True)
        if exact_result:
            return self.map_to_hca(exact_result)
        nearest_result = self.match_ontology(search, params, exact=False)
        if nearest_result:
            return self.map_to_hca(nearest_result)

    def match_ontology(self, search: str, params: dict, exact:bool = True):
        params['exact'] = exact
        results = self.perform_lookup(search, params)
        if results:
            index = self.matching_index(search, results)
            if index > -1:
                return results[index]

    def perform_lookup(self, term: str, params: dict):
        url = f'{self.url}/select'
        params['q'] = quote(term)
        response = requests.get(url=url, params=params)
        response.raise_for_status()
        return response.json().get('response', {}).get('docs', [])

    @staticmethod
    def matching_index(search: str, results: list) -> int:
        if len(results) == 1:
            return 0
        for index, result in enumerate(results):
            if result.get('label', '').lower() == search.lower():
                return index
            if result.get('short_form') == search:
                return index
        return -1

    @staticmethod
    def map_to_hca(ols_result: dict):
        return {
            'ontology': ols_result.get('obo_id'),
            'ontology_label': ols_result.get('label'),
            'text': ols_result.get('label')
        }
