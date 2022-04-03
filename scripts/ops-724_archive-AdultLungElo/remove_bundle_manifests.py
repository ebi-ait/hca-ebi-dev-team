import json

import requests

INGEST_API = 'https://api.ingest.archive.data.humancellatlas.org'
TOKEN = 'insert-token-without-bearer-prefix'

# TODO could be loaded from file
process_uuids_to_exclude = [

]


def get(url: str):
    return requests.get(url, headers={'Content-type': 'application/json'})


def get_all(url: str, entity_type: str):
    r = get(url)
    r.raise_for_status()
    result = r.json()

    entities = result["_embedded"][entity_type] if '_embedded' in result else []
    yield from entities

    while 'next' in result['_links']:
        next_url = result['_links']['next']['href']
        r = get(next_url)
        r.raise_for_status()
        result = r.json()
        entities = result['_embedded'][entity_type]
        yield from entities
        print(f"GET {entity_type} {json.dumps(result['page'])}")


bundle_manifest_url = f'{INGEST_API}/submissionEnvelopes/623c8ca5b06b223527d2897e/bundleManifests'
bundle_manifests = get_all(bundle_manifest_url, 'bundleManifests')
manifest_by_process_uuid = {}

for manifest in bundle_manifests:
    for process_uuid in list(manifest.get('fileProcessMap').keys()):
        manifest_by_process_uuid[process_uuid] = manifest

process_uuid_to_manifest = {}
manifest_urls_to_delete = []
for process_uuid in process_uuids_to_exclude:
    manifest = manifest_by_process_uuid.get(process_uuid)
    manifest_url = manifest['_links']['self']['href']
    process_uuid_to_manifest[process_uuid] = manifest
    manifest_urls_to_delete.append(manifest_url)

with open('process_uuid_to_manifest.json', 'w') as f:
    json.dump(process_uuid_to_manifest, f)

for manifest_url in manifest_urls_to_delete:
    r = requests.delete(manifest_url,
                        headers={
                            'Content-type': 'application/json',
                            'Authorization': f'Bearer {TOKEN}'
                        })

    r.raise_for_status()
