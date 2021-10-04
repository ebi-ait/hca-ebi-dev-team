import pandas

URL = 'http://www.nxn.se/single-cell-studies/data.tsv'

class NxnDatabaseService():
    @staticmethod
    def get_data() -> [[]]:
        return pandas.read_csv(URL, sep='\t')
