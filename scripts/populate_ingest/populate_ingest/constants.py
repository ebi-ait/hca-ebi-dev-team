ACCESSION_PATTERNS = {
    "insdc_project_accessions": "^[D|E|S]RP[0-9]+$",
    "ega_accessions": "EGA[DS][0-9]{11}",
    "dbgap_accessions": "phs[0-9]{6}(\\.v[0-9])?(\\.p[0-9])?",
    "geo_series_accessions": "^GSE.*$",
    "array_express_accessions": "^E-....-.*$",
    "insdc_study_accessions": "^PRJ[E|N|D][a-zA-Z][0-9]+$",
    "biostudies_accessions": "^S-[A-Z]{4}[0-9]+$"
}

ORGANISMS = ['human', 'human, mouse', 'mouse, human']
TECHNIQUE = ['chromium', 'dronc-seq', 'drop-seq', 'smart-seq2', 'smarter', 'smarter (c1)']
MEASUREMENTS = ['rna-seq']