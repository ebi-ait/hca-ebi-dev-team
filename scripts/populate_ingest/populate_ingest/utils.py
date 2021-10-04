# --- core imports
import itertools
import re

# --- third party library imports
import Levenshtein


def reformat_technique(technique: str) -> list:
    return technique.strip().casefold().split('&')


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


def get_ingest_data_publications(ingest_data) -> list:
    return list(itertools.chain.from_iterable(
        [data.get('publications') for data in ingest_data if data.get('publications')]))
