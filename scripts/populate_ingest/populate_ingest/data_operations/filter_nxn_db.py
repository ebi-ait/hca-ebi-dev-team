# --- core imports
import functools
import logging

# --- application imports
from ..constants import ORGANISMS, TECHNIQUE, MEASUREMENTS
from ..utils import is_technique_eligible


class Filter:
    @staticmethod
    def filter_by_organism(nxn_data):
        return nxn_data[nxn_data['Organism'].str.casefold().isin(ORGANISMS)]

    @staticmethod
    def filter_by_technology(nxn_data):
        is_technique_eligible_partial = functools.partial(is_technique_eligible, eligible_techniques=TECHNIQUE)
        return nxn_data[nxn_data['Technique'].fillna('').apply(is_technique_eligible_partial)]

    @staticmethod
    def filter_by_measurements(nxn_data):
        return nxn_data[nxn_data['Measurement'].str.casefold().isin(MEASUREMENTS)]

    @staticmethod
    def filter_by_eligibility(nxn_data):
        logging.info(f'project count before filtering {len(nxn_data)}')

        filtered_nxn_data = Filter.filter_by_organism(nxn_data)
        logging.info(f'project count after filtering by organism {len(filtered_nxn_data)}')

        filtered_nxn_data = Filter.filter_by_technology(filtered_nxn_data)
        logging.info(f'project count after filtering by technology {len(filtered_nxn_data)}')

        filtered_nxn_data = Filter.filter_by_measurements(filtered_nxn_data)
        logging.info(f'project count after filtering by measurement {len(filtered_nxn_data)}')

        return filtered_nxn_data
