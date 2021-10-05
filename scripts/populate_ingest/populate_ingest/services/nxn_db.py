import pandas


class NxnDatabaseService():
    url = 'http://www.nxn.se/single-cell-studies/data.tsv'

    @staticmethod
    def get_data() -> [[]]:
        missing_values = ['-']
        df = pandas.read_csv(NxnDatabaseService.url, sep='\t', na_values=missing_values)
        return df
