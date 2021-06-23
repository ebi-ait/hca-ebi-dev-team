import json
import logging

import requests as rq


class IngestQuery:
    TOKEN = '<REPLACE WITH FRESH TOKEN>'
    BASE_URL = 'https://api.ingest.archive.data.humancellatlas.org'
    DEV_BASE_URL = 'https://api.ingest.dev.archive.data.humancellatlas.org'
    BASE_URL = DEV_BASE_URL  # for testing on dev

    @staticmethod
    def get_ingest_projects():
        url = IngestQuery.BASE_URL + '/projects/search/catalogue'
        projects = rq.get(url + "?size=1000", headers={'Authorization': IngestQuery.TOKEN}).json()
        projects = projects['_embedded']['projects']

        return projects

    @staticmethod
    def get_project_update_url_by_uuid(uuid):
        url = IngestQuery.BASE_URL + f'/projects/search/findByUuid?uuid={uuid}'
        response = rq.get(url)
        if response.status_code == 200:
            return response.json()['_links']['self']['href']

        return None

    @staticmethod
    def patch_project(project_update_url, patch_data):
        logging.info(f'Updating project (project url: {project_update_url}) with {patch_data}')
        response = rq.patch(project_update_url, data=json.dumps(patch_data), headers={'Authorization': IngestQuery.TOKEN, 'Content-Type': 'application/json'})
        if response.status_code != 200:
            logging.info(f'Project with url:{project_update_url} failed with patching this payload: {patch_data}')

    @staticmethod
    def get_projects_from_dts_from_sheet(sheet_path):
        with open(sheet_path, 'r') as f:
            dts = f.read().splitlines()

        dts = [row.split('\t') for row in dts]
        headers = dts.pop(0)
        list_projects = {}
        for row in dts:
            new_dict = {}
            for i in range(len(headers)):
                new_dict[headers[i]] = row[i]
            list_projects[new_dict.get('UUID')] = new_dict

        return list_projects

    @staticmethod
    def not_exists_by_doi(ingest_projects, dts_projects):
        exists = False
        not_in_ingest = {}
        for project_dts in dts_projects:
            for project_ingest in ingest_projects:
                for publication in project_ingest.get('content', {}).get('publications', []):
                    if str(publication.get('doi')).lower() == str(project_dts.get('doi')).lower():
                        exists = True
                        break
                if exists:
                    exists = False
                    break
            else:
                not_in_ingest[project_dts['dcp_id']] = project_dts

        return not_in_ingest

    @staticmethod
    def exists_by_doi(ingest_projects, dts_projects):
        exists = False
        in_ingest = {}
        for project_dts in dts_projects:
            for project_ingest in ingest_projects:
                for publication in project_ingest.get('content', {}).get('publications', []):
                    if str(publication.get('doi')).lower() == str(project_dts.get('doi')).lower():
                        exists = True
                        in_ingest[project_ingest.get('uuid').get('uuid')] = project_dts
                        break
                if exists:
                    exists = False
                    break

        return in_ingest

    @staticmethod
    def not_exists_by_geo_accession(ingest_projects, dts_projects):
        exists = False
        not_in_ingest = {}
        for project_dts in dts_projects:
            for project_ingest in ingest_projects:
                for geo in project_ingest.get('content', {}).get('geo_series_accessions', []):
                    if geo in project_dts['data_accession']:
                        exists = True
                        break
                if exists:
                    exists = False
                    break
            else:
                not_in_ingest[project_dts['dcp_id']] = project_dts

        return not_in_ingest

    @staticmethod
    def exists_by_geo_accession(ingest_projects, dts_projects):
        exists = False
        in_ingest = {}
        for project_dts in dts_projects:
            for project_ingest in ingest_projects:
                for geo in project_ingest.get('content', {}).get('geo_series_accessions', []):
                    if geo in project_dts['data_accession']:
                        exists = True
                        in_ingest[project_ingest.get('uuid').get('uuid')] = project_dts
                        break
                if exists:
                    exists = False
                    break

        return in_ingest

    @staticmethod
    def filter_by_is_in_catalogue(ingest_projects, dts_projects):
        not_in_cat = []
        for project_dts in dts_projects:
            for project_ingest in ingest_projects:
                if 'isInCatalogue' not in project_ingest or project_ingest.get('isInCatalogue') == False:
                    not_in_cat.append(project_dts)
                    break

        return not_in_cat

    @staticmethod
    def get_projects_without_organ(ingest_projects):
        project_with_missing_organ = {}
        for project in ingest_projects:
            if 'organ' not in project or project.get('organ') is None:
                project_with_missing_organ[project.get('uuid').get('uuid')] = project
            elif 'ontologies' not in project.get('organ') or project.get('organ').get('ontologies') is None:
                project_with_missing_organ[project.get('uuid').get('uuid')] = project
            elif len(project.get('organ').get('ontologies')) == 0:
                project_with_missing_organ[project.get('uuid').get('uuid')] = project

        return project_with_missing_organ

    @staticmethod
    def get_projects_without_technology(ingest_projects):
        project_with_missing_technology = {}
        for project in ingest_projects:
            if 'technology' not in project or project.get('technology') is None:
                project_with_missing_technology[project.get('uuid').get('uuid')] = project
            elif 'ontologies' not in project.get('technology') or project.get('technology').get('ontologies') is None:
                project_with_missing_technology[project.get('uuid').get('uuid')] = project
            elif len(project.get('technology').get('ontologies')) == 0:
                project_with_missing_technology[project.get('uuid').get('uuid')] = project

        return project_with_missing_technology

    @staticmethod
    def get_projects_without_publications(ingest_projects):
        project_with_missing_publications = {}
        for project in ingest_projects:
            if 'content' not in project or project.get('content') is None:
                project_with_missing_publications[project.get('uuid').get('uuid')] = project
            elif 'publications' not in project.get('content') or project.get('content').get('publications') is None:
                project_with_missing_publications[project.get('uuid').get('uuid')] = project
            elif len(project.get('content').get('publications')) == 0:
                project_with_missing_publications[project.get('uuid').get('uuid')] = project

        return project_with_missing_publications

    @staticmethod
    def get_projects_without_cell_count(ingest_projects):
        project_with_missing_cell_count = {}
        for project in ingest_projects:
            if 'cellCount' not in project or project.get('cellCount') is None:
                project_with_missing_cell_count[project.get('uuid').get('uuid')] = project

        return project_with_missing_cell_count

