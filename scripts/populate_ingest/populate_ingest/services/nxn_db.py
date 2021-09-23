import requests

class NxnDatabaseService():
    URL = 'http://www.nxn.se/single-cell-studies/data.tsv'

    @staticmethod
    def get_data() -> [[]]:
        # Get nxn's database as tsv and transform it into a matrix
        text = NxnDatabaseService.get_nxn_text()
        response = text.splitlines()
        response = [data.split("\t") for data in response]
        return response

    @staticmethod
    def get_nxn_text():
        response = requests.get(NxnDatabaseService.URL, headers={'Cache-Control': 'no-cache'})
        response.raise_for_status()
        response.encoding = 'utf-8'  # Avoid issues with special chars
        text = response.text
        return text