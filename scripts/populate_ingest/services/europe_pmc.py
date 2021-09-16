import requests


class EuropePmc:
    def __init__(self, url: str = None) -> None:
        self.url = url if url else 'https://www.ebi.ac.uk/europepmc/webservices/rest/search'
        
    def query_doi(self, doi: str):
        params = {
            'query': 'doi:' + doi,
            'resultType': 'core',
            'format': 'json'
            }
        response = requests.get(self.url, params=params)
        response.raise_for_status()
        result = response.json().get('resultList', {}).get('result', [])
        if len(result) > 0:
            return result.pop()
