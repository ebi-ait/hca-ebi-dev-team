# --- core imports
import argparse
import json
import logging
import pprint
import sys

# --- application imports
import config
from .convert.europe_pmc import EuropePmcConverter
from .convert.nxn_db import NxnDatabaseConverter
from .data_operations.compare_ingest_nxn_db import Compare
from .data_operations.filter_nxn_db import Filter
from .services.europe_pmc import EuropePmc
from .services.ingest import QuickIngest
from .services.nxn_db import NxnDatabaseService


def prepare_logging():
    logging.basicConfig(filename='nxn_db.log', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    logging.getLogger('').addHandler(console)

    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        logging.error('Exception', exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = handle_exception


class Populate:
    def __init__(self, ingest_service, nxn_db_service: NxnDatabaseService, nxn_db_converter: NxnDatabaseConverter):
        self.ingest_service = ingest_service
        self.ingest_data = [data.get('content') for data in self.ingest_service.get_projects()]
        self.nxn_data = nxn_db_service.get_data()
        self.nxn_db_converter = nxn_db_converter

    def populate(self, write):
        new_nxn_data = Compare.compare_and_get_new_data(self.ingest_data, self.nxn_data)
        logging.info(f'Found {len(new_nxn_data)} new projects in nxn database, after comparing with ingest')
        new_nxn_data = Filter.filter_by_eligibility(new_nxn_data)
        logging.info(f'Found {len(new_nxn_data)} projects in nxn database, after filtering by eligibility criteria')
        projects_to_be_added = self.nxn_db_converter.convert(new_nxn_data)
        added_projects_uuids = self.__add_projects(projects_to_be_added, write)

        return projects_to_be_added, added_projects_uuids

    def __add_projects(self, project_list, write):
        added_projects_uuids = []
        for project in project_list:
            if write:
                try:
                    response = self.ingest_service.new_project(project)
                    uuid = response.get('uuid', {}).get('uuid')
                    added_projects_uuids.append(uuid)
                    logging.debug(f'added to ingest with uuid {uuid}')
                except:
                    logging.exception('')
        return added_projects_uuids


def run(write):
    prepare_logging()
    logging.info(f'Running script to populate ingest with data from nxn db')
    logging.info(f"Running program in {'write' if write else 'dry run'} mode")

    ingest_service = QuickIngest(url=config.INGEST_API_URL, token=config.INGEST_API_TOKEN)
    ingest_schema = ingest_service.get_schemas(high_level_entity='type',
                                                     domain_entity='project',
                                                     concrete_entity="project")[0]['_links']['json-schema']['href']
    nxn_database_converter = NxnDatabaseConverter(ingest_schema=ingest_schema, publication_service=EuropePmc(), publication_converter=EuropePmcConverter())
    populate = Populate(ingest_service=ingest_service, nxn_db_service= NxnDatabaseService, nxn_db_converter=nxn_database_converter)
    logging.info('Finding entries in nxn db to add to ingest')
    projects_to_be_added, added_projects_uuids = populate.populate(write)
    logging.info(f'Successfully added {len(added_projects_uuids)} project(s) to ingest')

    if projects_to_be_added:
        with open('projects_to_be_added.json', 'w') as f:
            json.dump(projects_to_be_added, f)
    if added_projects_uuids:
        with open('added_uuids.txt', mode='wt', encoding='utf-8') as f:
            f.write('\n'.join(added_projects_uuids))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Add projects to ingest from Valentine's / NXN database")
    parser.add_argument('-w', '--write', action='store_true', help='Write to ingest')

    args = parser.parse_args()
    write = args.write

    run(write)
