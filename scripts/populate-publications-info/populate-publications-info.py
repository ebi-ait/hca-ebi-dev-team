import argparse, json, requests

def get_publications_journal(publications):
    # Use crossref API to get extra meta info
    # This should be replicated in ingest API endpoint when we have an endpoint
    # Not done on client side for speed
    results = []
    for publication in publications:
        try:
            crossref = requests.get(f"https://api.crossref.org/works/{publication['doi']}").json()['message']
            if len(crossref['container-title']) > 0:
                journal_title = crossref['container-title'][0]
            elif "name" in crossref['institution']:
                # BioRxiv is listed under institution
                journal_title = crossref['institution']['name']
            else:
                journal_title = crossref['publisher']

            results.append({
                "doi": publication['doi'],
                "url": crossref['URL'],
                "journalTitle": journal_title,
                "title": publication['title'],
                "authors": publication['authors']
            })
        except:
            print(f"Something went wrong retrieving metainformation for publication {publication['doi']}")
    return results

def is_in_dcp(uuid):
    azul_proj_url = f'https://service.azul.data.humancellatlas.org/index/projects/{uuid}'
    if requests.get(azul_proj_url):
        return True
    return False

def get_project(uuid, base_url):
    project_url = f'{base_url}/projects/search/findByUuid?uuid={uuid}'
    try:
        response = requests.get(project_url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f'Error getting project {uuid}: {e}')
    

def patch_project(uuid, project, token):
    project_patch = {}
    if project["isInCatalogue"] == False:
        project_patch["isInCatalogue"] = True
    
    if "publications" in project["content"]:
        if not project["publicationsInfo"]:
            project_patch["publicationsInfo"] = get_publications_journal(project["content"]["publications"])
    
    if project["wranglingState"] != "Published in DCP" and is_in_dcp(uuid):
        project_patch["wranglingState"] = "Published in DCP"

    if not project_patch:
        print(f"Patch unnecessary for project UUID: {uuid}")
        return None

    try:
        print(f"Updating project {uuid}: {project_patch}")
        update_url = f'{project["_links"]["self"]["href"]}?partial=true'
        headers={'Authorization': token, 'Content-Type': 'application/json'}
        data = json.dumps(project_patch)
        r = requests.patch(update_url, data=data, headers=headers)
        r.raise_for_status()
    except Exception as e:
        print(f'Error patching project {uuid}: {e}')

def get_uuids_from_catalogue(base_url):
    catalogue_url = f'{base_url}/projects/search/catalogue?page=0&size=500'
    res = requests.get(catalogue_url)
    res.raise_for_status()
    for project in res.json()['_embedded']['projects']:
        yield project['uuid']['uuid']
        

def get_uuids(input_file):
    with open(input_file, "r") as file:
        return file.read().splitlines()


def get_token(input_file):
    with open(input_file, "r") as file:
        return file.read()


if __name__ == "__main__":
    description = "Update projects in ingest to use the project catalogue and add publicationsInfo"
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-i", "--input", help="File containing a list of UUIDs to scrape. Each UUID must be on a new line.", default="published_uuids.txt")
    parser.add_argument("-u", "--url", help="Base URL for Ingest API", default="https://api.ingest.dev.archive.data.humancellatlas.org")
    parser.add_argument("-t", "--token", help="Text file containing an ingest token", default="~/token.txt")
    parser.add_argument("-c", "--use_catalogued", action="store_true", help="Use projects that are already included in the catalogue without specifying an input file. This is used for updating publicationsInfo")

    args = parser.parse_args()

    if(args.use_catalogued):
        uuids = get_uuids_from_catalogue(args.url)
    else:
        uuids = get_uuids(args.input)

    token = get_token(args.token)

    for uuid in uuids:
        project = get_project(uuid, args.url)
        if project:
            patch_project(uuid, project, token)