# --- core imports
import logging

# --- application imports
from ..constants import ORGANISMS, TECHNIQUE, MEASUREMENTS
from ..utils import reformat_technique

class Filter:
    @staticmethod
    def filter_by_organism(nxn_data):
        return nxn_data[nxn_data['Organism'].str.casefold().isin(ORGANISMS)]

    # todo: gotta fix the nan issue here
    @staticmethod
    def filter_by_technology(nxn_data):
        return nxn_data[nxn_data['Technique'].apply(reformat_technique).isin(TECHNIQUE)]

    @staticmethod
    def filter_by_measurements(nxn_data):
        return nxn_data[nxn_data['Measurement'].str.casefold().isin(MEASUREMENTS)]

    @staticmethod
    def filter_by_eligibility(nxn_data):
        logging.info(f'project count before filtering {len(nxn_data)}')

        filtered_nxn_data = Filter.filter_by_organism(nxn_data)
        logging.info(f'project count after filtering by organism {len(filtered_nxn_data)}')

        # filtered_nxn_data = Filter.filter_by_technology(filtered_nxn_data)
        logging.info(f'project count after filtering by technology {len(filtered_nxn_data)}')

        filtered_nxn_data = Filter.filter_by_measurements(filtered_nxn_data)
        logging.info(f'project count after filtering by measurement {len(filtered_nxn_data)}')

        return filtered_nxn_data
