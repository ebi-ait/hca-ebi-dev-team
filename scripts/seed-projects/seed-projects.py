import argparse, json, requests
from faker import Faker
from random import randint

def create_fake_publication(fake):
    return {
        "doi": fake.isbn13(), # Not a real doi
        "url": fake.url(),
        "journalTitle": fake.sentence(3),
        "title": fake.sentence(15),
        "authors": [ fake.name() for i in range(8) ]
    }

def create_fake_contributor(fake):
    return {
        "name": fake.name(),
        "email": fake.email(),
        "institution": fake.company(),
        "corresponding_contributor": False
    }

def create_project(fake, catalogued, ingest_url, token):
    project = {
        "content": {
            "contributors": [ create_fake_contributor(fake) for i in range(randint(1,10)) ],
            "describedBy": "https://schema.dev.data.humancellatlas.org/type/project/14.3.0/project",
            "funders": [{
                "grant_id": fake.sentence(4),
                "organization": fake.company()
            }],
            "project_core": {
                "project_short_name": fake.password(10),
                "project_title": fake.sentence(10),
                "project_description": fake.paragraph(4)
            },
            "publications": [{
                "authors": [ fake.name() for i in range(8) ],
                "title": fake.sentence(15)
            }],
            "schema_type": "project"
        },
        "isInCatalogue": catalogued,
        "organ": {
            "ontologies": [{
                "text": "future glans",
                "ontology": "UBERON:0013238",
                "ontology_label": "future glans"
            }]
        },
        "technology": {
            "ontologies": [{
                "text": "sci-RNA-seq",
                "ontology": "EFO:0010550",
                "ontology_label": "sci-RNA-seq"
            }]
        },
        "identifyingOrganisms": ["Human"],
        "releaseDate": "2024-03-10T23:00:00.000Z",
        "dataAccess": {
            "type": "All fully open"
        },
        "publicationsInfo": [ create_fake_publication(fake) for i in range(randint(1,3)) ]
    }

    try:
        url = f'{ingest_url}/projects'
        headers={'Authorization': token}
        r = requests.post(url, json=project, headers=headers)
        r.raise_for_status()
        uuid = r.json()["uuid"]["uuid"]
        print(f"Created project with uuid: {uuid}")
    except Exception as e:
        print(f'Error creating project: {e}')

def get_token(input_file):
    with open(input_file, "r") as file:
        return file.read()


if __name__ == "__main__":
    description = "Seed ingest API with projects"
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-u", "--url", help="Base URL for Ingest API", default="https://api.ingest.dev.archive.data.humancellatlas.org")
    parser.add_argument("-n", "--number", help="Number of fake projects to create", default="1")
    parser.add_argument("-t", "--token", help="Text file containing an ingest token", default="~/token.txt")
    parser.add_argument("-c", "--catalogued", help="Should the projects be in the project catalogue?", action="store_true")

    args = parser.parse_args()

    if "api.ingest.archive.data.humancellatlas.org" in args.url:
        raise IOError("Cannot run this script on prod ingest API")

    token = get_token(args.token)


    for i in range(0, int(args.number)):
        Faker.seed(i)
        fake = Faker()
        create_project(fake, args.catalogued, args.url, token)
