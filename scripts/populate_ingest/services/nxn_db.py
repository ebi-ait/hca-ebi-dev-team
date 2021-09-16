import requests

class NxnDatabaseService():
    URL = 'http://www.nxn.se/single-cell-studies/data.tsv'

    @staticmethod
    def get_data(self) -> [[]]:
        # Get nxn's database as tsv and transform it into a matrix
        response = requests.get(self.URL, headers={'Cache-Control': 'no-cache'})
        response.raise_for_status()
        response.encoding = 'utf-8'  # Avoid issues with special chars
        response = response.text.splitlines()
        response = [data.split("\t") for data in response]
        return response

