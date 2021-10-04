import re
from json_converter.json_mapper import JsonMapper
from submission_broker.submission.entity import Entity
from ..services.ontology import QuickOntology
from .conversion_utils import map_value, append, get_accessions

ACCESSION_PATTERNS = {
    "insdc_project_accessions": "^[D|E|S]RP[0-9]+$",
    "ega_accessions": "EGA[DS][0-9]{11}",
    "dbgap_accessions": "phs[0-9]{6}(\\.v[0-9])?(\\.p[0-9])?",
    "geo_series_accessions": "^GSE.*$",
    "array_express_accessions": "^E-....-.*$",
    "insdc_study_accessions": "^PRJ[E|N|D][a-zA-Z][0-9]+$",
    "biostudies_accessions": "^S-[A-Z]{4}[0-9]+$"
}
ACCESS_MAP = {
    'open': 'All fully open',
    'managed': 'All managed access',
    'mixed': 'A mixture of open and managed'
}
ORGANISM = {
    'human': ['Human'],
    'human&mouse': ['Human', 'Mouse']
}

PROJECT_SPEC = {
    'identifyingOrganisms': ['organism', map_value, ORGANISM],
    'dataAccess': {
        'type': ['access_permission', map_value, ACCESS_MAP]
    },
    'cellCount': ['cell_count_estimate'],
    'wranglingNotes': ['comments', append, f'; AutoImported Snapshot 2021-06-03'],
}
FIXED_VALUES = {
    'wranglingState': 'Eligible',
    'wranglingPriority': 3,
    'isInCatalogue': True,
}


class DatasetTrackerConverter:
    def __init__(self, lookup: QuickOntology) -> None:
        self.spec = PROJECT_SPEC
        self.lookup = lookup

    def convert(self, project: Entity):
        input_project = project.attributes
        converted_project = JsonMapper(input_project).map(self.spec)
        converted_project.update(FIXED_VALUES)
        
        technologies = self.get_ontologies(project, 'assay_type', self.lookup.get_technology)
        if technologies:
            converted_project.setdefault('technology', {})['ontologies'] = technologies
        
        organ_ontologies = self.get_ontologies(project, 'organ', self.lookup.get_organ)
        if organ_ontologies:
            converted_project.setdefault('organ', {})['ontologies'] = organ_ontologies

        accessions = get_accessions(input_project.get('data_accession', ''), accession_patterns=ACCESSION_PATTERNS)
        converted_project.setdefault('content', {}).update(accessions)
        return converted_project

    @staticmethod
    def get_ontologies(project: Entity, key: str, lookup_method):
        ontologies = []
        if key in project.attributes:
            for term in project.attributes.get(key).split(','):
                term = term.strip()
                if term:
                    ontology = lookup_method(term, project)
                    if ontology:
                        ontologies.append(ontology)
        return ontologies
