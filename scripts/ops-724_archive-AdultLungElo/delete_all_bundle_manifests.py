import requests
from ingest.api.ingestapi import IngestApi

TOKEN = 'insert-bearer-token-with-prefix'
INGEST_API = 'https://api.ingest.archive.data.humancellatlas.org'
ingest_api = IngestApi(url=INGEST_API)
ingest_api.set_token(f'Bearer {TOKEN}')
headers = {
    'Content-type': 'text/uri-list',
    'Authorization': f'Bearer {TOKEN}'
}


def delete_entity(entity):
    uri = entity["_links"]['self']["href"]
    r = requests.delete(uri, headers=headers)
    print(f'removed entity {uri}')
    r.raise_for_status()


bundle_manifest_url = f'{INGEST_API}/submissionEnvelopes/623c8ca5b06b223527d2897e/bundleManifests'
bundle_manifests = list(ingest_api.get_all(bundle_manifest_url, 'bundleManifests'))

for bundle_manifest in bundle_manifests:
    delete_entity(bundle_manifest)