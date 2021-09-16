# --- core imports
import argparse
from datetime import datetime
import itertools
import logging
import pprint
import re
import sys

# --- third party library imports
import Levenshtein

# --- application imports
from convert.conversion_utils import get_accessions
from convert.europe_pmc import EuropePmcConverter
from data_entities.nxn_db import NxnDatabase
from services.europe_pmc import EuropePmc
from services.nxn_db import NxnDatabaseService
from services.ingest import QuickIngest


# INGEST_URL = "https://api.ingest.archive.data.humancellatlas.org"
INGEST_URL = "http://localhost:8080"

# utility functions
def reformat_title(title: str) -> str:
    return re.sub("\W", "", title).lower().strip()

def get_distance_metric(title1: str,title2: str):
    if not all([title1, title2]):
        return 0
    max_len = max(len(title1), len(title2))
    dist_metric = 100-(Levenshtein.distance(title1, title2)/max_len)*100
    return dist_metric

def get_file_content(file_path):
    with open(file_path, "r") as file_path:
        return file_path.read()

def prepare_logging():
    logging.basicConfig(filename='nxn_db.log', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        logging.error("Exception", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = handle_exception

class Populate:
    def __init__(self, url, token, write):
        self.write = write
        self.ingest_api = QuickIngest(url, token=get_file_content(token))
        self.ingest_data = [data.get("content") for data in self.ingest_api.get_all_projects()]
        self.nxn_data = NxnDatabase(NxnDatabaseService.get_data())
        self.europe_pmc = EuropePmc()
        self.publication_converter = EuropePmcConverter()

    def __compare_on_doi__(self):
        ingest_data_pubs = list(itertools.chain.from_iterable(
            [data.get("publications") for data in self.ingest_data if data.get("publications")]))
        ingest_data_pub_doi = {pub.get("doi") for pub in ingest_data_pubs if pub.get("doi")}
        ingest_data_pub_urls = {pub.get("url") for pub in ingest_data_pubs if pub.get("url")}
        ingest_data_pre_doi = {url.split('doi.org/')[1] for url in ingest_data_pub_urls if 'doi.org/' in url}

        filter_doi = (self.nxn_data.get_values('DOI') | self.nxn_data.get_values('bioRxiv DOI')) - (
                    ingest_data_pub_doi | ingest_data_pre_doi)
        self.nxn_data.data = [row for row in self.nxn_data.data if self.nxn_data.get_value(row, 'DOI') in filter_doi or
                              self.nxn_data.get_value(row, 'bioRxiv DOI') in filter_doi]

    def __compare_on_accession__(self):
        ingest_data_accessions = set(itertools.chain.from_iterable(
            [data.get("insdc_project_accessions") for data in self.ingest_data if
             data.get("insdc_project_accessions")] +
            [data.get("geo_series_accessions") for data in self.ingest_data if data.get("geo_series_accessions")] +
            [data.get("ega_accessions") for data in self.ingest_data if data.get("ega_accessions")] +
            [data.get("dbgap_accessions") for data in self.ingest_data if data.get("dbgap_accessions")] +
            [data.get("array_express_accessions") for data in self.ingest_data if
             data.get("array_express_accessions")] +
            [data.get("biostudies_accessions") for data in self.ingest_data if data.get("biostudies_accessions")] +
            [data.get("insdc_study_accessions") for data in self.ingest_data if data.get("insdc_study_accessions")]))

        filter_accessions = self.nxn_data.get_values('Data location') - ingest_data_accessions
        self.nxn_data.data = [row for row in self.nxn_data.data if self.nxn_data.get_value(row, 'Data location') in filter_accessions
                              or not self.nxn_data.get_value(row, 'Data location')]

    def __compare_on_title__(self):
        ingest_data_pubs = list(itertools.chain.from_iterable([data.get("publications") for data in self.ingest_data if data.get("publications")]))
        ingest_data_titles = set([reformat_title(pub.get("title")) for pub in ingest_data_pubs if pub.get("title")])

        filter_titles = {reformat_title(title) for title in self.nxn_data.get_values('Title')} - ingest_data_titles
        filter_titles = {title for title in filter_titles if not any([get_distance_metric(title, tracking_title)
                                                                >= 97 for tracking_title in ingest_data_titles])}
        self.nxn_data.data = [row for row in self.nxn_data.data if reformat_title(self.nxn_data.get_value(row, 'Title')) in filter_titles]

    def compare(self):
        self.__compare_on_doi__()
        self.__compare_on_accession__()
        self.__compare_on_title__()

    def filter(self):
        self.nxn_data.data = [row for row in self.nxn_data.data if
                         self.nxn_data.get_value(row, 'Organism').lower() in ["human", "human, mouse", "mouse, human"]]
        self.nxn_data.data = [row for row in self.nxn_data.data if
                         any([tech.strip() in ["chromium", "drop-seq", "dronc-seq", "smart-seq2", "smarter",
                                               "smarter (C1)"] for tech in
                              self.nxn_data.get_value(row, 'Technique').lower().split("&")])]
        self.nxn_data.data = [row for row in self.nxn_data.data if self.nxn_data.get_value(row, 'Measurement').lower() == 'rna-seq']

    def __convert__(self, nxn_data_row) -> dict:
        #  wb schema? does it get set via ingest api?
        ingest_project = {
            'content': {},
            'cellCount': self.nxn_data.get_value(nxn_data_row, 'Reported cells total'),
            'identifyingOrganisms': [organism.strip() for organism in
                                     self.nxn_data.get_value(nxn_data_row, 'Organism').split(',')],
            'isInCatalogue': True,
            'wranglingNotes': f"Auto imported from nxn db {datetime.today().strftime('%Y-%m-%d')}"
        }

        # setting project title, project description, funders, contributors and publication and publicationsInfo
        publication_info = self.europe_pmc.query_doi(self.nxn_data.get_value(nxn_data_row, 'DOI'))
        if publication_info:
            publications, info = self.publication_converter.convert(publication_info)
            ingest_project['content'].update(publications)
            ingest_project['publicationsInfo'] = info

        # setting project short name
        ingest_project['content'].setdefault('project_core', {}).setdefault('project_short_name', 'tba')

        # setting accessions
        ingest_project['content'].update(get_accessions(self.nxn_data.get_value(nxn_data_row, 'DOI')))
        return ingest_project

    def add_projects(self):
        for nxn_data_row in self.nxn_data.data:
            project = self.__convert__(nxn_data_row)
            logging.info(f'Converted nxn data row: {nxn_data_row} to \n'
                         f'ingest project: {pprint.pformat(project)}' )
            if self.write:
                response = self.ingest_api.new_project(project)
                uuid = response.get('uuid', {}).get('uuid')
                print(f'added to ingest with uuid {uuid}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add projects to ingest from Valentine's / NXN database")
    parser.add_argument("-u", "--url", type=str, help="Base URL for Ingest API", default=INGEST_URL)
    parser.add_argument("-tp", "--token-path", type=str, help="Text file containing an ingest token", required=True)
    parser.add_argument("-w", "--write", action='store_true', help="Write to ingest")

    args = parser.parse_args()

    prepare_logging()

    logging.info(f"Running program in {'write' if args.write else 'dry run'} mode")
    populate = Populate(args.url, args.token_path, args.write)
    logging.info('Finding and filtering entries in nxn db, to add to ingest')
    populate.compare()
    populate.filter()
    logging.info(f'found {len(populate.nxn_data.data)} nxn entries to add to ingest')

    populate.add_projects()

