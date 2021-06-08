import re

from json_converter.json_mapper import JsonMapper
from .conversion_utils import map_value, append

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
    'wranglingNotes': ['comments', append, f'; AutoImported Snapshot 2021-06-03'],
}
FIXED_VALUES = {
    'wranglingState': 'Eligible',
    'wranglingPriority': 3,
    'isInCatalogue': True,
}


class DatasetTrackerConverter:
    def __init__(self) -> None:
        self.spec = PROJECT_SPEC

    def convert(self, project: dict):
        converted_project = JsonMapper(project).map(self.spec)
        converted_project.update(FIXED_VALUES)

        accessions = self.get_accessions(project.get('data_accession', ''))
        converted_project.setdefault('content', {}).update(accessions)
        # ToDo: Map for technology, organ?
        return converted_project
    
    @staticmethod
    def get_accessions(data_accessions: str):
        accessions = {}
        for accession in data_accessions.split(','):
            accession = accession.strip()
            for key, pattern in ACCESSION_PATTERNS.items():
                regex = re.compile(pattern)
                if regex.match(accession):
                    accessions.setdefault(key, []).append(accession)
        return accessions

    @staticmethod
    def get_publication_info():
        pass
