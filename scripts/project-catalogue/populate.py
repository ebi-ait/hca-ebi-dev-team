import argparse
import json
import os
from typing import List, Tuple

from requests.models import HTTPError

from excel.load import SheetLoader, Entity
from convert.tracker import DatasetTrackerConverter
from convert.europe_pmc import EuropePmcConverter
from services.europe_pmc import EuropePmc
from services.ingest import QuickIngest

SHEET = "Group 1"
URL = "https://api.ingest.dev.archive.data.humancellatlas.org"
TOKEN = "source/token.txt"


class Populate:
    def __init__(self, file_path, sheet=SHEET, url=URL, token_path=TOKEN):
        self.ingest = QuickIngest(url, token=self.get_token(token_path))
        self.path = file_path
        self.sheet = sheet
        loader = SheetLoader(self.path, self.sheet)
        self.submission = loader.data
        self.europe_pmc = EuropePmc()
        self.sheet_converter = DatasetTrackerConverter()
        self.publication_converter = EuropePmcConverter()

    def sort_projects(self) -> Tuple[List[Entity], List[Entity]]:
        new_projects = []
        existing_projects = []
        for project in self.submission.get_entities(self.sheet):
            doi = project.attributes.get('doi', '')
            project_uuid = project.attributes.get('ingest_project_uuid', '')
            if (
                    (doi and self.ingest.doi_exists(doi)) or
                    (project_uuid and self.ingest.project_exists(project_uuid))
            ):
                existing_projects.append(project)
            else:
                new_projects.append(project)
        return new_projects, existing_projects

    def post_projects(self, projects: List[Entity]):
        for project in projects:
            conversion = self.convert_project(project)
            self.post_project(project, conversion)

    def convert_project(self, project: Entity):
        conversion = self.sheet_converter.convert(project.attributes)
        self.add_publication_info(conversion, project)
        self.set_defaults(conversion, project)
        return conversion

    def add_publication_info(self, conversion: dict, project: Entity):
        doi = project.attributes.get('doi', '')
        if doi:
            publication_info = self.europe_pmc.query_doi(doi)
            if publication_info:
                publications, info = self.publication_converter.convert(publication_info)
                conversion.setdefault('content', {}).update(publications)
                conversion['publicationsInfo'] = info

    @staticmethod
    def set_defaults(conversion: dict, project: Entity):
        default_title = project.attributes.get('pub_title', '')
        conversion.setdefault('content', {}).setdefault('project_core', {}).setdefault('project_title', default_title)
        conversion.setdefault('content', {}).setdefault('project_core', {}).setdefault('project_short_name', project.identifier.index)

    def post_project(self, project: Entity, conversion: dict):
        try:
            document = self.ingest.new_project(conversion)
            uuid = document.get('uuid', {}).get('uuid')
            if uuid:
                project.add_accession('ingest_project', uuid)
                project.attributes['ingest_project_uuid'] = uuid
                return
            project.add_error('ingest_project_uuid', f'Could not add project: {conversion}, response: {document}')
        except HTTPError as e:
            project.add_error('ingest_project_uuid', f'Could not add project: {conversion}, error: {e}')

    def save(self, new_projects: List[Entity], ignored_projects: List[Entity]):
        inserted_projects, errored_projects = self.make_inserted_errored_lists(new_projects)
        document = {
            'inserted': inserted_projects,
            'errored': errored_projects,
            'ignored': self.make_ignored_list(ignored_projects)
        }
        file_path = os.path.splitext(self.path)[0] + ".json"
        self.write_dict(file_path, document)

    @staticmethod
    def make_inserted_errored_lists(projects: List[Entity]):
        inserted = {}
        errored = {}
        for project in projects:
            if project.has_errors():
                errored[project.identifier.index] = project.get_errors().get('ingest_project_uuid', ['Unknown Error'])
            else:
                inserted[project.identifier.index] = project.get_accession('ingest_project')
        return inserted, errored

    @staticmethod
    def make_ignored_list(projects: List[Entity]):
        output = []
        for project in projects:
            output.append(project.identifier.index)
        return output

    @staticmethod
    def get_token(token_path):
        with open(token_path, "r") as token_file:
            return token_file.read()

    @staticmethod
    def write_dict(file_path: str, data: dict):
        file_path = os.path.abspath(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, "w") as open_file:
            json.dump(data, open_file, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add projects to ingest from datatracker export")
    parser.add_argument('file_path', type=str, help="Excel file exported from datatracker.")
    parser.add_argument("-s", "--sheet", type=str, help="Name of sheet to import", default=SHEET)
    parser.add_argument("-u", "--url", type=str, help="Base URL for Ingest API", default=URL)
    parser.add_argument("-t", "--token_path", type=str, help="Text file containing an ingest token", default=TOKEN)
    args = parser.parse_args()

    populate = Populate(args.file_path, args.sheet, args.url, args.token_path)
    new, existing = populate.sort_projects()
    populate.post_projects(new)
    populate.save(new, existing)
