import argparse
from copy import deepcopy
import json
import os
from typing import List, Tuple

from requests.models import HTTPError
from assertpy import assert_that
from mergedeep import merge

from data_entities.load import SheetLoader, Entity
from convert.tracker import DatasetTrackerConverter
from convert.europe_pmc import EuropePmcConverter
from services.europe_pmc import EuropePmc
from services.ingest import QuickIngest
from services.ontology import QuickOntology

SHEET = "Group 1"
URL = "https://api.ingest.dev.archive.data.humancellatlas.org"
TOKEN = "source/token.txt"
ACCESSIONS = "source/accessions.json"
ALLOWED_PATCH_FIELDS = [
    "primaryWrangler",
    "secondaryWrangler",
    "wranglingState",
    "wranglingPriority",
    "wranglingNotes",
    "cellCount",
    "dataAccess",
    "identifyingOrganisms",
    "technology",
    "organ",
    "isInCatalogue",
    "publicationsInfo"
]


class Populate:
    def __init__(self, file_path, sheet=SHEET, url=URL, token_path=TOKEN, simulate=False):
        self.ingest = QuickIngest(url, token=self.get_token(token_path))
        self.path = file_path
        self.sheet = sheet
        loader = SheetLoader(self.path, self.sheet)
        self.submission = loader.data
        self.europe_pmc = EuropePmc()
        self.sheet_converter = DatasetTrackerConverter(lookup=QuickOntology())
        self.publication_converter = EuropePmcConverter()
        self.simulate = simulate
        self.inserted = []
        self.updated = []
        self.ignored = []
        self.failed = []

    def add_accessions(self, accessions: dict):
        for dcp_id, ingest_uuid in accessions.items():
            project = self.submission.get_entity(self.sheet, dcp_id)
            if project:
                project.attributes['ingest_project_uuid'] = ingest_uuid

    def sort_projects(self) -> Tuple[List[Entity], List[Entity]]:
        new_projects = []
        existing_projects = []
        for sheet_project in self.submission.get_entities(self.sheet):
            doi = sheet_project.attributes.get('doi', '')
            project_uuid = sheet_project.attributes.get('ingest_project_uuid', '')
            if (
                    (doi and self.ingest.doi_exists(doi)) or
                    (project_uuid and self.ingest.project_exists(project_uuid))
            ):
                existing_projects.append(sheet_project)
            else:
                new_projects.append(sheet_project)
        return new_projects, existing_projects

    def post_projects(self, projects: List[Entity]):
        for sheet_project in projects:
            conversion = self.convert_project(sheet_project)
            if self.simulate:
                sheet_project.attributes['post'] = conversion
                self.inserted.append(sheet_project)
            else:
                self.post_project(sheet_project, conversion)

    def post_project(self, project: Entity, conversion: dict):
        try:
            document = self.ingest.new_project(conversion)
            uuid = document.get('uuid', {}).get('uuid')
            if uuid:
                project.add_accession('ingest_project', uuid)
                self.inserted.append(project)
                return
            project.add_error('ingest_project_uuid', f'Could not add project: {conversion}, response: {document}')
        except HTTPError as e:
            project.add_error('ingest_project_uuid', f'Could not add project: {conversion}, error: {e}')
        self.failed.append(project)

    def update_projects(self, projects: List[Entity]):
        for sheet_project in projects:
            ingest_project = self.get_ingest_project(sheet_project)
            if not ingest_project:
                self.ignored.append(sheet_project)
                continue
            new_project = self.convert_project(sheet_project)
            project_patch = self.make_project_patch(ingest_project, new_project)
            project_needs_patch = self.project_needs_patch(ingest_project, project_patch)
            if not project_needs_patch:
                self.ignored.append(sheet_project)
                continue
            if self.simulate:
                sheet_project.attributes['patch'] = project_patch
                self.updated.append(sheet_project)
                continue
            patch_url = self.ingest.get_link_from_resource(ingest_project, 'self')
            try:
                self.ingest.patch(patch_url, project_patch)
                self.updated.append(sheet_project)
            except HTTPError as e:
                sheet_project.add_error('ingest_project_uuid', f'Could not update project: {patch_url}, with patch: {project_patch}, error: {e}')
                self.failed.append(sheet_project)

    def get_ingest_project(self, sheet_project: Entity):
        uuid = sheet_project.attributes.get('ingest_project_uuid')
        if uuid:
            try:
                return self.ingest.get_project_by_uuid(uuid)
            except HTTPError as e:
                sheet_project.add_error('ingest_project_uuid', f'Could not find Project by UUID: {uuid}, error: {e}')
        doi = sheet_project.attributes.get('doi')
        if not doi:
            sheet_project.add_error('ingest_project_uuid', f'No UUID and No DOI found for project: {sheet_project.identifier.index}')
            return
        ingest_projects = self.ingest.get_projects_by_doi(doi)
        if len(ingest_projects) == 1:
            sheet_project.attributes['ingest_project_uuid'] = ingest_projects[0].get('uuid', {}).get('uuid')
            return ingest_projects[0]
        sheet_project.add_error('doi', f'No UUID and {"too many" if len(ingest_projects) > 1 else "no"} ingest projects for DOI: {doi}')

    def convert_project(self, project: Entity):
        conversion = self.sheet_converter.convert(project)
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

    def save(self):
        document = {
            'totals': {
                'inserted': len(self.inserted),
                'updated': len(self.updated),
                'failed': len(self.failed),
                'ignored': len(self.ignored)
            },
            'inserted': self.make_map(self.inserted),
            'updated': self.make_map(self.updated),
            'failed': self.make_error_map(self.failed),
            'ignored': self.make_list(self.ignored)
        }
        file_path = os.path.splitext(self.path)[0] + ".json"
        self.write_dict(file_path, document)
        full_file_path = os.path.splitext(self.path)[0] + "_full.json"
        self.write_dict(full_file_path, self.submission.as_dict(string_lists=True))

    @staticmethod
    def set_defaults(conversion: dict, project: Entity):
        default_title = project.attributes.get('pub_title', '')
        conversion.setdefault('content', {}).setdefault('project_core', {}).setdefault('project_title', default_title)
        conversion.setdefault('content', {}).setdefault('project_core', {}).setdefault('project_short_name', project.identifier.index)

    @staticmethod
    def make_project_patch(original: dict, new: dict) -> dict:
        full_patch = merge({}, original, new)
        project_patch = {k: full_patch[k] for k in ALLOWED_PATCH_FIELDS}
        return project_patch

    @staticmethod
    def project_needs_patch(project: dict, patch: dict) -> bool:
        patched_project = deepcopy(project)
        patched_project.update(patch)
        try:
            assert_that(project).is_equal_to(patched_project)
            return False
        except AssertionError:
            return True

    @staticmethod
    def make_map(projects: List[Entity]) -> dict:
        inserted = {}
        for project in projects:
            uuid = project.get_accession('ingest_project')
            if not uuid:
                uuid = project.attributes.get('ingest_project_uuid')
            if uuid:
                inserted[project.identifier.index] = uuid
        return inserted

    @staticmethod
    def make_list(projects: List[Entity]) -> List[str]:
        output = []
        for project in projects:
            output.append(project.identifier.index)
        return output

    @staticmethod
    def make_error_map(projects: List[Entity]) -> dict:
        errored = {}
        for project in projects:
            errored[project.identifier.index] = project.get_errors()
        return errored

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
    parser.add_argument("--sheet", type=str, help="Name of sheet to import", default=SHEET)
    parser.add_argument("--url", type=str, help="Base URL for Ingest API", default=URL)
    parser.add_argument("--token_path", type=str, help="Text file containing an ingest token", default=TOKEN)
    parser.add_argument("--accession_file", type=str, help="Text file containing accessions", default=ACCESSIONS)
    parser.add_argument("--simulate", action='store_true', help="Take no action")

    args = parser.parse_args()

    populate = Populate(args.file_path, args.sheet, args.url, args.token_path, args.simulate)
    if args.accession_file:
        file_accessions = {}
        with open(args.accession_file) as accession_file:
            file_accessions = json.load(accession_file)
        populate.add_accessions(file_accessions)
    insert, update = populate.sort_projects()
    populate.post_projects(insert)
    populate.update_projects(update)
    populate.save()
