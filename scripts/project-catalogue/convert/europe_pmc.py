from typing import List
from json_converter.json_mapper import JsonMapper
from .conversion_utils import remove_tags, first_map


CONTENT_SPEC = {
    'project_core': {
        'project_title': ['title'],
        'project_description': ['abstractText', remove_tags, '']
    }
}
PUBLICATION_SPEC = {
    'doi': ['doi'],
    'pmid': ['pmid'],
    'title': ['title'],
    'authors': ['authorString'],
    'url': ['fullTextUrl.url']
}
PUBLICATION_INFO_SPEC = {
    "doi": ['doi'],
    "url": ['fullTextUrlList'],
    "journalTitle": ['journalTitle'],
    "url": ['fullTextUrl.url'],
    "title": ['title'],
}
CONTRIBUTOR_SPEC = {
    'first': ['firstName'],
    'last': ['lastName'],
    'institution': ['authorAffiliationDetailsList.authorAffiliation', first_map, 'affiliation'],
    'orcid_id': ['authorId.value']
}
FUNDER_SPEC = {
    'grant_id': ['grantId'],
    'organization': ['agency']
}


class EuropePmcConverter:
    @staticmethod
    def convert(publication: dict):
        # Only want one url from the list
        if 'fullTextUrlList' in publication and 'fullTextUrl' in publication['fullTextUrlList'] and len(publication['fullTextUrlList']['fullTextUrl']) > 0:
            publication['fullTextUrl'] = publication['fullTextUrlList']['fullTextUrl'][0]

        converted_project = JsonMapper(publication).map(CONTENT_SPEC)
        converted_project['contributors'] = EuropePmcConverter.convert_contributors(publication.get('authorList', {}).get('author', []))
        converted_project['funders'] = EuropePmcConverter.convert_funders(publication.get('grantsList', {}).get('grant', []))
        converted_project['publications'], authors = EuropePmcConverter.convert_publications(publication)
        info = EuropePmcConverter.convert_publications_info(publication, authors)
        return converted_project, info

    @staticmethod
    def convert_publications(publication_info: dict):
        publications = []
        publication = JsonMapper(publication_info).map(PUBLICATION_SPEC)
        authors = publication.get('authors', '').split(', ')
        if authors:
            publication['authors'] = authors
        if publication:
            publications.append(publication)
        return publications, authors
    
    @staticmethod
    def convert_publications_info(publication_info: dict, authors: list):
        publications = []

        if 'journalInfo' in publication_info:
            publication_info['journalTitle'] = publication_info['journalInfo']['journal']['title']
        elif 'bookOrReportDetails' in publication_info:
            # Cater for the edge case of BioRxiv. BioRxiv is pre-print so not listed under journalInfo
            publication_info['journalTitle'] = publication_info['bookOrReportDetails']['publisher']
        
        publications_info = JsonMapper(publication_info).map(PUBLICATION_INFO_SPEC)
        if authors:
            publications_info['authors'] = authors
        publications.append(publications_info)
        return publications

    @staticmethod
    def convert_contributors(authors: List[dict]):
        contributors = []
        for author in authors:
            contributor = JsonMapper(author).map(CONTRIBUTOR_SPEC)
            if 'first' in contributor and 'last' in contributor:
                first_name = contributor.pop('first')
                last_name = contributor.pop('last')
                name = f'{first_name},,{last_name}'
                contributor['name'] = name
            if contributor:
                contributors.append(contributor)
        return contributors
    
    @staticmethod
    def convert_funders(grants: List[dict]):
        funders = []
        for grant in grants:
            funder = JsonMapper(grant).map(FUNDER_SPEC)
            if funder:
                funders.append(funder)
        return funders
