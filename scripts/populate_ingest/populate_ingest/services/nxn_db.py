import pandas

URL = 'http://www.nxn.se/single-cell-studies/data.tsv'

class NxnDatabaseService():
    @staticmethod
    def get_data() -> [[]]:
        missing_values = ['-']
        df = pandas.read_csv(URL, sep='\t', na_values=missing_values)
        return df
