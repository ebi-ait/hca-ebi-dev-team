import json

import requests

INGEST_API = 'https://api.ingest.archive.data.humancellatlas.org'
TOKEN = 'insert-token-without-bearer-prefix'

# TODO could be loaded from file
process_uuids_to_exclude = [
"440d5068-3e8e-4cd2-9424-72b48ddec093",
"f69570cd-b9dd-47c4-b3c8-fb7e7dffb445",
"9bfa7137-daa6-4d65-91d2-68cf3dc6f8d3",
"06b0de15-c702-45cf-befc-d570b60b13e7",
"198d86af-4f88-42fc-b6f8-2d66e9088802",
"80c35ab7-323d-49e5-9844-76b79e08d480",
"28a80262-2afb-4937-b9c4-a7a227ed8227",
"7f990904-c8ed-4ece-94e4-e22761d17b51",
"f0fe754c-27ef-4b8f-806a-684732f76aca",
"63d5a3ec-07b3-4dcd-a023-c6698bf95d0d",
"490f54a3-2b82-42b4-b763-7d9e7000ed7a",
"92f9fbdf-cbdb-4c76-b5fa-4e4402c54a1f",
"491c6208-b50e-4265-aa75-16a1365c14a2",
"5b04cfd9-3ffe-48d0-889a-e3ebbd5d5ba5",
"696b61f3-c1fa-4b2f-8140-37d95d5ae2ba",
"f9fb3d80-0a49-4086-9743-9a946d0b3f1d",
"24960e4e-55cc-4513-a1cb-f8b7ddf62bcb",
"bd90a1cd-c7f7-4c6a-98b9-b809e571b6b1",
"3998e753-a339-42b7-8b08-89acafa51a51",
"ae12c2af-2961-483f-9cc8-14a6df25cdbb",
"202281e9-e74e-4b26-b33f-b41e95a1c7f3",
"530b2cfa-354e-4311-ad80-439be614847e",
"b3813668-8d3a-416c-a3c1-b1a86d6cd6c5",
"78c6a52a-65f8-47a8-9e42-d8c309f60f07",
"afe0e5be-b162-43f4-9354-7ffccb1dc2c5",
"a5b8ea57-242a-4baa-8a83-4313567a2d95",
"eb5f509a-e7c2-4cf0-ac46-3e0bb6225a7b",
"7ef213ae-9ea1-4227-994e-ca83a8f78453",
"a6b5ad01-6dc7-4455-8df4-f34bda779d15",
"71d475d1-4a27-4958-9e16-ca14606b1a7d",
"dfed8c53-2ec5-4305-9f2d-132b226a3fb4",
"be090691-f79b-42d0-a9b0-2cf48908184d",
"9788b865-f91a-48b1-8151-898bef819331",
"7c9e706f-159d-4d22-aa86-fb8dff5d67df",
"ac3b5ec7-229c-4ce4-a2ab-dd9a248a35a5",
"d30fe5ad-9140-4390-afc3-a2696ac0581d",
"be253361-03f6-4fd2-85ce-4775529b9628",
"6e2fe1f7-6f5b-43f7-b1fc-0b7afeb720ee",
"1d811ade-3ec1-4948-81d7-0f5d454eb28b",
"ba08a609-7a96-4a6d-9ac9-0d2fd0207668",
"31fadfd6-a5f0-4951-8940-b1a8825f1b4a",
"cd901249-9354-4c50-bf71-d8383e0469c7",
"12e51576-020d-468b-8ac4-9a2c5c851a08",
"0495d0e2-b181-472f-814b-badae69f0cb2",
"6e41a4e8-174a-4b2b-88b4-9dfd6310de40",
"ee052188-1901-4c8b-937a-9984fe217f9c",
"f9c8bcc6-bc54-4b8e-9c27-b84573c6e3a4",
"eddc24e9-ca8e-4286-89c1-80e8fa598730",
"85ca1445-6d1a-4fdb-8af8-07aa260663df",
"ce538079-1054-469c-b661-ee6906136723",
"dcceebb2-99dc-4873-aefa-cd1a4264b896",
"c3ca365a-720c-4ff4-83ef-c55c6c4d562e",
"67895497-4d85-42ca-8b37-d162d8c775ea",
"8ae0924e-fc43-4f5b-b14e-581358c118c6",
"2acc2be1-6b98-4653-beb6-74d761414c37",
"393ee435-8310-419d-9daf-4c7cd2e1f814",
"ccb85400-3393-48f1-aac2-20248d356495",
"9ad7a042-dae9-4a84-9934-0e5c05c046b4",
"ef641347-f30a-478e-bc84-a4ca2dbe8a07",
"e7f791ba-273f-47b0-82a4-89b7f2f4fefc",
"24e3f9e8-f59b-4140-b45f-23895d22fc10",
"38d0fb8a-272e-481a-b9a9-68afdee7d28d",
"d4210bcc-c292-4fe4-ab50-5b92dc0ad9bb",
"f6544603-a68b-4325-8545-8a7b2148ee7b",
"5b60de21-ad4a-4c91-9238-9afd7c51515a",
"72cce498-2ea7-4dc2-8eaa-f2058b5171dd",
"5a5c8173-2ac8-4741-aba9-248c81348e6a",
"707497bb-8f6c-49c3-9e57-d383a9ea3dd1",
"cff85207-1e35-4d3d-8af7-4a53f1bf8a7f",
"f2a4ef0c-9531-4b40-b4b3-91e63403306f",
"5535aec3-d7b9-414c-81d6-00d77a48810d",
"3c65e5ee-75c3-40a6-abdc-be56ec0c4940",
"f5445747-7371-4e98-889e-29ed4d337b25",
"d22bacc7-6041-4548-a823-4d6b1f49b8a0",
"991b5468-067e-4455-9a07-15048a516579",
"360bc524-73b2-4829-bcfa-05564a435a42",
"9d063780-3fd7-4e95-b100-34f129c734a6",
"cfaf3128-b592-49df-828d-6d1267f2d416",
"a0424ffb-17e6-40e6-8272-c0834b98823f",
"7e5057e5-9260-444b-bd02-d97c90dd790c",
"e8e3417a-eb45-4f65-ba73-a887a58d1cf5",
"883ab8e3-1e95-4eca-8a29-5729afcc08f2",
"a59789b4-4d3c-42e5-bde4-7b764dc6d778",
"614828f9-0cd9-4c94-b19e-44caf564afed",
"5fe228aa-cf58-4344-8f04-65f03014a7ce",
"385857e7-244b-4608-88b4-5326e4f880a6",
"1a0b6015-2094-49a4-b639-20c75bab8bb1",
"11082d42-8607-4969-bc88-c8118c5eb67e",
"246a2618-3f87-45c1-bded-3ca9e87d3e59",
"60a0bc5d-2733-408e-a59a-c7fe1c89c1aa",
"58e75e5a-bd32-48bb-88f5-b93f38ccda20",
"7da9f8eb-9569-4ab1-a4db-510d8320face",
"4e6723d8-d5f5-4c29-b3d6-92a43242bb83",
"fafed346-54d6-4ada-8a78-8dece29d6a04",
"4dd351ca-687a-46b9-90c1-1edaf9109922",
"ba487554-fc5f-4cac-b31a-467832940ad3",
"d4ee83ec-97f8-496e-9101-194d16a41b8a",
"a02ccf9d-722e-4521-9a69-e61e9483bc78"

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
