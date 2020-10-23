import json
import sys
from copy import deepcopy


def retrieve_metadata_entities(uuid_mapping, filename_staging_area_list):
    mapping_to_files = deepcopy(uuid_mapping)
    for entity_type, uuid_dict in uuid_mapping.items():
        for uuid, id in uuid_dict.items():
            for filename in filename_staging_area_list:
                if entity_type in filename and uuid in filename and not "descriptor" in filename:
                    mapping_to_files[entity_type][uuid] = filename
                    break
    return mapping_to_files

def retrieve_data_entities(uuid_mapping, filename_staging_area_list):
    data_files_mapping = {}
    data_files = [filename for filename in filename_staging_area_list if "metadata" not in filename and "descriptor" not in filename]
    sequence_filename_list = list(uuid_mapping['sequence_file'].values())
    for filename in data_files:
        for sequence_filename in sequence_filename_list:
            if sequence_filename in filename:
                data_files_mapping[sequence_filename] = filename
                break
    return data_files_mapping

def retrieve_descriptors(uuid_mapping, filename_staging_area_list):
    file_descriptors_mapping = {}
    descriptors = [filename for filename in filename_staging_area_list if "descriptor" in filename]

    sequence_file_uuid = list(uuid_mapping['sequence_file'].keys())
    for filename in descriptors:
        for sequence_uuid in sequence_file_uuid:
            if sequence_uuid in filename:
                file_descriptors_mapping[sequence_uuid] = filename
                break
    return file_descriptors_mapping


def retrieve_links(project_uuid, filename_staging_area_list):
    links = [filename for filename in filename_staging_area_list if "links" in filename]
    links_mapping = {}
    for filename in links:
        if project_uuid in filename:
            links_mapping[filename.split('links/')[1].split("_")[0]] = filename
    return links_mapping

def main(uuid_mapping, filename_staging_area_list):
    with open(uuid_mapping, 'r') as f:
        uuid_dict = json.load(f)
    with open(filename_staging_area_list, 'r') as f:
        filenames_staging = f.read().splitlines()

    file_mapping = retrieve_metadata_entities(uuid_dict, filenames_staging)
    file_mapping['file_descriptors'] = retrieve_descriptors(uuid_dict, filenames_staging)
    file_mapping['data_files'] = retrieve_data_entities(uuid_dict, filenames_staging)
    file_mapping['links'] = retrieve_links(list(uuid_dict['project'].keys())[0], filenames_staging)

    new_filename = f"staging_{uuid_mapping.split('/')[-1]}"
    with open(new_filename, 'w') as f:
        json.dump(file_mapping, f, indent=4, separators=(',', ': '))



if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])