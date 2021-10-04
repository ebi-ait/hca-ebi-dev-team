import re


def get_accessions(data_accessions: str, accession_patterns: dict):
    accessions = {}
    for accession in data_accessions.split(','):
        accession = accession.strip()
        for key, pattern in accession_patterns.items():
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


