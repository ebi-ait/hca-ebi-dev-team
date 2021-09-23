import re


ACCESSION_PATTERNS = {
    "insdc_project_accessions": "^[D|E|S]RP[0-9]+$",
    "ega_accessions": "EGA[DS][0-9]{11}",
    "dbgap_accessions": "phs[0-9]{6}(\\.v[0-9])?(\\.p[0-9])?",
    "geo_series_accessions": "^GSE.*$",
    "array_express_accessions": "^E-....-.*$",
    "insdc_study_accessions": "^PRJ[E|N|D][a-zA-Z][0-9]+$",
    "biostudies_accessions": "^S-[A-Z]{4}[0-9]+$"
}

def get_accessions(data_accessions: str):
    accessions = {}
    for accession in data_accessions.split(','):
        accession = accession.strip()
        for key, pattern in ACCESSION_PATTERNS.items():
            regex = re.compile(pattern)
            if regex.match(accession):
                accessions.setdefault(key, []).append(accession)
    return accessions

def fixed_attribute(*args):
    value = args[1]
    return value


def map_value(*args):
    key = args[0]
    if isinstance(args[1], dict):
        return args[1].get(key, '')


def remove_tags(*args):
    regex = re.compile(r'<([^>]+)>')
    if isinstance(args[0], str):
        return regex.sub('', args[0])


def first_map(*args):
    array = args[0]
    key = args[1]
    if isinstance(array, list) and len(array) > 0 and isinstance(array[0], dict):
        return array[0].get(key, None)


def append(*args):
    pre = args[0]
    post_script = args[1]
    if pre and post_script:
        return pre + post_script


