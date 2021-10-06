# --- core imports
import itertools
import re

# --- third party library imports
import Levenshtein
import pandas


def reformat_technique(technique: str) -> list:
    return [t.strip() for t in technique.casefold().split('&')]


def is_technique_eligible(technique: str, eligible_techniques) -> bool:
    return not set(reformat_technique(technique)).isdisjoint(eligible_techniques)


def reformat_title(title: str) -> str:
    return re.sub("\W", "", title).lower().strip()


def get_distance_metric(title1: str, title2: str):
    if not all([title1, title2]):
        return 0
    max_len = max(len(title1), len(title2))
    dist_metric = 100 - (Levenshtein.distance(title1, title2) / max_len) * 100
    return dist_metric


def get_ingest_data_contents(ingest_data) -> list:
    return [data.get('content') for data in ingest_data]


def get_ingest_data_publications(ingest_projects) -> list:
    return list(itertools.chain.from_iterable(
        [data.get('publications') for data in ingest_projects if data.get('publications')]))


def get_accessions(data_accessions: str, accession_patterns: dict):
    accessions = {}
    for accession in data_accessions.split(','):
        accession = accession.strip()
        for key, pattern in accession_patterns.items():
            regex = re.compile(pattern)
            if regex.match(accession):
                accessions.setdefault(key, []).append(accession)
    return accessions


def not_is_nan(x):
    return not pandas.isna(x)


def remove_tags(*args):
    regex = re.compile(r'<([^>]+)>')
    if isinstance(args[0], str):
        return regex.sub('', args[0])


def first_map(*args):
    array = args[0]
    key = args[1]
    if isinstance(array, list) and len(array) > 0 and isinstance(array[0], dict):
        return array[0].get(key, None)


def convert_pmid(*args):
    pmid = args[0]
    if pmid and isinstance(pmid, str):
        return int(pmid)
    return None