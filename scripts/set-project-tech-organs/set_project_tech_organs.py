'''
load/create the following
api_object
dataset_tracker_sheet

for a given set of project uuids

check whether the organs and technologies fields have data.
if yes, store the data, else continue

if the project has a submission,
examine the metadata in the submission and store a unique list of organ/model organ/organ part/model organ part
ontology objects

examine the metadata in the submission and store a unique list of technology ontology objects

else if the project does not have a submission:
lookup the project in the dataset_tracker_sheet
get the list of organs and ontologise
get the list of technologies and ontologise
log results so they can be reviewed and errors manually curated

'''

import getopt, argparse, json, requests, time
import pandas as pd
from ingest.api.ingestapi import IngestApi
import pprint
import re


class Project:
    def __init__(self, uuid, ingest_api, organs={}, technologies={}):
        self.existing_organs = organs
        self.existing_technologies = technologies
        self.update_organs = {}
        self.update_technologies = {}
        self.uuid = uuid
        self.current_json = ingest_api.get_project_by_uuid(self.uuid)
        self.mongo_id = self.current_json['_links']['self']['href'].rsplit('/', 1)[-1]
        self.submission_count = self.count_submissions()

        if 'organ' in self.current_json.keys() and self.current_json['organ']:
            for organ in self.current_json['organ']['ontologies']:
                self.existing_organs[organ['ontology']] = organ
        if 'technology' in self.current_json.keys() and self.current_json['technology']:
            for tech in self.current_json['technology']['ontologies']:
                self.existing_technologies[tech['ontology']] = tech

    def __str__(self):
        return "Project with uuid {}\nmongo id: {}\nSubmission count:{}\nexisting organs: {}\nexisting techs: " \
               "{}\nupdate organs: {}\nupdate_techs:{}".format(
            self.uuid, self.mongo_id, self.submission_count, self.existing_organs, self.existing_technologies,
            self.update_organs, self.update_technologies)

    def count_submissions(self):
        response = requests.get(self.current_json['_links']['submissionEnvelopes']['href']).json()
        if '_embedded' in response.keys():
            return len(response['_embedded'])
        else:
            return 0

    def _set_update_organs(self, biomaterial_json):
        """add an organ to the update_organs dictionary"""
        if re.search('specimen_from_organism', biomaterial_json['content']['describedBy']):
            self.update_organs[biomaterial_json['content']['organ']['ontology']] = biomaterial_json['content']['organ']
        elif re.search('cell_line', biomaterial_json['content']['describedBy']):
            self.update_organs[biomaterial_json['content']['model_organ']['ontology']] = biomaterial_json['content'][
                'model_organ']
        elif re.search('organoid', biomaterial_json['content']['describedBy']):
            self.update_organs[biomaterial_json['content']['model_organ']['ontology']] = biomaterial_json['content'][
                'model_organ']

    def _set_update_technologies(self, protocol_json):
        """Add a technology to the update_technologies dictionary"""
        if re.search('library_preparation_protocol', protocol_json['content']['describedBy']):
            self.update_technologies[protocol_json['content']['library_construction_method']['ontology']] = \
            protocol_json['content']['library_construction_method']

    def get_from_metadata(self, ingest_api):
        """ get the organ and technology metadata from an ingest submission """
        project_json = ingest_api.get_project_by_uuid(uuid=self.uuid)
        submission_json = ingest_api.get_submission(project_json['_links']['submissionEnvelopes']['href'])
        for sub_env in submission_json['_embedded']['submissionEnvelopes']:
            biomaterials_json = requests.get(sub_env['_links']['biomaterials']['href']).json()
            for page in range(0, biomaterials_json['page']['totalPages']):
                paged_api_link = sub_env['_links']['biomaterials']['href'] + "?page=" + str(page)
                biomaterials = requests.get(paged_api_link).json()['_embedded']['biomaterials']
                for biomaterial in biomaterials:
                    if re.search('cell_suspension', biomaterial['content']['describedBy']):
                        break
                    else:
                        self._set_update_organs(biomaterial)

            protocols_json = requests.get(sub_env['_links']['protocols']['href']).json()
            for page in range(0, protocols_json['page']['totalPages']):
                paged_api_link = sub_env['_links']['protocols']['href'] + "?page=" + str(page)
                protocols_json = requests.get(paged_api_link).json()
                for protocol in protocols_json['_embedded']['protocols']:
                    self._set_update_technologies(protocol)
        print("project {} updated from ingest".format(self.uuid))

    def get_from_tracker(self, tracker, tech_dict):
        """Get organ and tech metadata from the tracking sheet"""
        tracker_row = tracker[tracker['ingest_project_uuid'] == self.uuid].to_dict()
        if len(tracker_row['dcp_id']) == 0:
            print("No information found in tracker for this uuid")
        else:
            tracker_organs = tracker_row['organ'][list(tracker_row['organ'].keys())[0]].split(',')
            tracker_organs = [organ.strip() for organ in tracker_organs]
            tracker_techs = tracker_row['assay_type'][list(tracker_row['assay_type'].keys())[0]].split(',')
            tracker_techs = [tech.strip() for tech in tracker_techs]
            for organ in tracker_organs:
                ontologised_organ = ontologise_term('uberon', 'http://purl.obolibrary.org/obo/UBERON_0000465', organ)
                self.update_organs[ontologised_organ['ontology']] = ontologised_organ
            for tech in tracker_techs:
                ontologised_tech = tech_dict[tech]
                self.update_technologies[ontologised_tech['ontology']] = ontologised_tech

    def merge_properties(self):
        """merges the update properties with the existing properties so each ontology only occurs once"""
        self.update_organs = {**self.update_organs, **self.existing_organs}
        self.update_technologies = {**self.update_technologies, **self.existing_technologies}

    def update_project(self, ingest_api_url, auth_token):
        """Submit patch request to update the technology and organ fields of the project with the update properties."""
        api_url = '{}/projects/{}?partial=true'.format(ingest_api_url, self.mongo_id)
        print(api_url)
        payload = {}
        organ_list = list(self.update_organs.values())
        tech_list = list(self.update_technologies.values())
        payload['technology'] = {"ontologies": tech_list}
        payload['organ'] = {"ontologies": organ_list}
        pprint.pprint(payload)
        submission_headers = {'Authorization': 'Bearer {}'.format(auth_token),
                              'Content-Type': 'application/json'}
        response = requests.patch(api_url,
                                  data=json.dumps(payload),
                                  headers=submission_headers)
        return response


def ontologise_term(allowed_ontology, graph_restriction, term):
    ols_api_url = 'http://www.ebi.ac.uk/ols/api/search?q='
    request_url = "{}{}&ontology={}&allChildrenOf={}".format(ols_api_url, term, allowed_ontology, graph_restriction)
    response = requests.get(request_url).json()
    for curation in response['response']['docs']:
        if curation['label'].lower() == term.lower():
            return {'text': term,
                    'ontology': curation['obo_id'],
                    'ontology_label': curation['label']}
    print('no exact match found, using first result')
    first_curation = response['response']['docs'][0]
    return {'text': term,
            'ontology': first_curation['obo_id'],
            'ontology_label': first_curation['label']}


def define_parser():
    parser = argparse.ArgumentParser(description="Parser for the arguments")
    parser.add_argument("--uuids", "-u", action="store", dest="uuid_file", type=str,
                        help="path to text file with list of uuid")
    parser.add_argument("--auth_token", "-t", action="store", dest="auth_token", type=str,
                        help="auth token to allow updating via the ui")
    parser.add_argument("--environment", "-e", action="store", dest="env", type=str,
                        help="environment you want to submit to", default="prod")
    parser.add_argument("--tech_dict", "-d", action="store", dest="tech_dict", type=str,
                        help="path to a csv that has ontology curations for each technology")
    return parser


def load_dataset_tracker():
    download_link = "https://docs.google.com/spreadsheets/d/1rm5NZQjE-9rZ2YmK_HwjW-LgvFTTLs7Q6MzHbhPftRE/export?gid=0&format=tsv"
    tracker_df = pd.read_csv(download_link, sep="\t")
    return tracker_df


def load_tech_dict(path_to_csv):
    tech_csv = pd.read_csv(path_to_csv)
    tech_dict = {}
    for index, row in tech_csv.iterrows():
        tech_dict[row['text']] = {'text': row['text'],
                                  'ontology': row['ontology'],
                                  'ontology_label': row['ontology_label']}
    return tech_dict


def main(args):
    tracker = load_dataset_tracker()
    tech_dict = load_tech_dict(args.tech_dict)

    with open(args.uuid_file, 'r') as file:
        uuid_list = file.read().splitlines()

    if args.env == "prod":
        env = ""
    elif args.env == "staging":
        env = "staging."
    else:
        env = "dev."
    ingest_api_url = "http://api.ingest.{}archive.data.humancellatlas.org".format(env)
    ingest_api = IngestApi(ingest_api_url)
    project_list = [Project(uuid, ingest_api) for uuid in uuid_list]

    for project in project_list:
        if project.submission_count > 0:
            project.get_from_metadata(ingest_api)
        else:
            project.get_from_tracker(tracker, tech_dict)
        project.merge_properties()
        response = project.update_project(ingest_api_url, args.auth_token)
        if response['status_code'] is 200:
            print("Project {} successfully updated in ingest database".format(project.uuid))
        else:
            print("There was a problem with updating project {} in ingest database".format(project.uuid))
            print(response['status_code'])


if __name__ == "__main__":
    parser = define_parser()
    args = parser.parse_args()
    main(args)
