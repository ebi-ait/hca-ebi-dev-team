# --- core imports
import logging

# --- application imports
from ..constants import ACCESSION_PATTERNS
from ..utils import reformat_title, get_distance_metric, get_ingest_data_publications


class Compare:
    @staticmethod
    def compare_on_doi(ingest_data, nxn_data):
        ingest_data_pubs = get_ingest_data_publications(ingest_data)
        ingest_data_pub_doi = {pub.get('doi') for pub in ingest_data_pubs if pub.get('doi')}
        ingest_data_pre_doi = {pub.get('url').split('doi.org/')[1] for pub in ingest_data_pubs
                               if pub.get('url') and 'doi.org/' in pub.get('url')}

        nxn_doi = set(nxn_data['DOI'].unique())
        nxn_biorxiv_doi = set(nxn_data['bioRxiv DOI'].dropna().unique())

        new_doi = (nxn_doi | nxn_biorxiv_doi) - (
                ingest_data_pub_doi | ingest_data_pre_doi)

        return nxn_data[nxn_data[['DOI', 'bioRxiv DOI']].isin(new_doi).any(1)]

    @staticmethod
    def compare_on_accessions(ingest_data, nxn_data):
        ingest_data_accessions = []

        for data in ingest_data:
            for accession_type in ACCESSION_PATTERNS:
                if data.get(accession_type):
                    ingest_data_accessions.extend(data.get(accession_type))

        new_accessions = set(nxn_data['Data location'].dropna().unique()) - set(ingest_data_accessions)

        return nxn_data[nxn_data['Data location'].isin(new_accessions) | nxn_data['Data location'].isna()]

    @staticmethod
    def compare_on_title(ingest_data, nxn_data):
        ingest_data_pubs = get_ingest_data_publications(ingest_data)
        ingest_data_titles = set([reformat_title(pub.get('title')) for pub in ingest_data_pubs if pub.get('title')])

        new_titles = {reformat_title(title) for title in set(nxn_data['Title'].unique())} - ingest_data_titles
        new_titles = {title for title in new_titles if not any([get_distance_metric(title, ingest_title)
                                                                >= 97 for ingest_title in ingest_data_titles])}

        return nxn_data[nxn_data['Title'].apply(reformat_title).isin(new_titles)]

    @staticmethod
    def compare_and_get_new_data(ingest_data, nxn_data):
        logging.info('Comparing ingest data with nxn data')
        new_nxn_data = Compare.compare_on_doi(ingest_data, nxn_data)
        logging.info(f'project count after comparing by doi {len(new_nxn_data)}')
        new_nxn_data = Compare.compare_on_accessions(ingest_data, new_nxn_data)
        logging.info(f'project count after comparing by accessions {len(new_nxn_data)}')
        new_nxn_data = Compare.compare_on_title(ingest_data, new_nxn_data)
        logging.info(f'project count after comparing by title {len(new_nxn_data)}')

        return new_nxn_data


