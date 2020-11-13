import json
import os
import sys
from copy import deepcopy

OUTPUT_DIR = 'outdir'
ALL_FILES_FILENAME = f'all_files.json'
ALL_FILES_BY_PROJECT_FILENAME = f'all_files_by_project.json'
SUMMARY_FILENAME = f'staging_summary.json'


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
    data_files = [filename for filename in filename_staging_area_list if
                  "metadata" not in filename and "descriptor" not in filename]
    sequence_filename_list = list(uuid_mapping['sequence_file'].values())

    supplementary_filename_list = []
    if (uuid_mapping.get('supplementary_file')):
        supplementary_filename_list = list(uuid_mapping['supplementary_file'].values())

    for filename in data_files:
        for sequence_filename in sequence_filename_list:
            if sequence_filename in filename:
                data_files_mapping[sequence_filename] = filename
                break
        for supplementary_filename in supplementary_filename_list:
            if supplementary_filename in filename:
                data_files_mapping[supplementary_filename] = filename
                break

    return data_files_mapping


def retrieve_descriptors(uuid_mapping, filename_staging_area_list):
    file_descriptors_mapping = {}
    descriptors = [filename for filename in filename_staging_area_list if "descriptor" in filename]

    sequence_file_uuid = list(uuid_mapping['sequence_file'].keys())

    supplementary_file_uuids = []
    if (uuid_mapping.get('supplementary_file')):
        supplementary_file_uuids = list(uuid_mapping['supplementary_file'].keys())

    for filename in descriptors:
        for sequence_uuid in sequence_file_uuid:
            if sequence_uuid in filename:
                file_descriptors_mapping[sequence_uuid] = filename
                break
        for supplementary_file_uuid in supplementary_file_uuids:
            if supplementary_file_uuid in filename:
                file_descriptors_mapping[supplementary_file_uuid] = filename
                break

    return file_descriptors_mapping


def retrieve_links(project_uuid, filename_staging_area_list):
    links = [filename for filename in filename_staging_area_list if "links" in filename]
    links_mapping = {}
    for filename in links:
        if project_uuid in filename:
            links_mapping[filename.split('links/')[1].split("_")[0]] = filename
    return links_mapping


def main(project_uuid, uuid_dict, filenames_staging):
    file_mapping = retrieve_metadata_entities(uuid_dict, filenames_staging)
    file_mapping['file_descriptors'] = retrieve_descriptors(uuid_dict, filenames_staging)
    file_mapping['data_files'] = retrieve_data_entities(uuid_dict, filenames_staging)
    file_mapping['links'] = retrieve_links(project_uuid, filenames_staging)

    summary = {}
    count = 0
    for entity_type, value in file_mapping.items():
        summary[entity_type] = len(value.keys())
        count = count + summary[entity_type]

    new_filename = f"{OUTPUT_DIR}/staging_{uuid_mapping_filename.split('/')[-1]}"
    with open(new_filename, 'w') as f:
        print(f'Writing {new_filename}')
        json.dump(file_mapping, f, indent=4, separators=(',', ': '))

    return file_mapping, summary, count


if __name__ == '__main__':
    mapping_files_dir_path = sys.argv[1]
    ls_staging_area_file_path = sys.argv[2]

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    all_data = None
    all_summary = {}
    all_count = 0
    all_files_by_project = {}
    all_files = []
    for map_file in os.listdir(mapping_files_dir_path):
        if map_file.endswith(".json"):
            uuid_mapping_filename = os.path.join(mapping_files_dir_path, map_file)
            print(f'Reading {uuid_mapping_filename}')
            with open(uuid_mapping_filename, 'r') as f:
                uuid_dict = json.load(f)
            with open(ls_staging_area_file_path, 'r') as f:
                filenames_staging = f.read().splitlines()

            project_uuid = None
            if uuid_dict.get('project'):
                project_uuid = list(uuid_dict['project'].keys())[0]
            else:
                raise ValueError(f'{uuid_mapping_filename} has no project')

            all_data, summary, count = main(project_uuid, uuid_dict, filenames_staging)
            all_summary[map_file] = summary
            all_count = all_count + count

            for entity_type, file_map in all_data.items():
                for entity_uuid, file_path in file_map.items():
                    if not all_files_by_project.get(project_uuid):
                        all_files_by_project[project_uuid] = {}

                    if not all_files_by_project[project_uuid].get(file_path):
                        all_files.append(file_path)

                    # Use dict to remove duplicates
                    all_files_by_project[project_uuid][file_path] = file_path

    print(f'Writing {OUTPUT_DIR}/{SUMMARY_FILENAME}')
    with open(f'{OUTPUT_DIR}/{SUMMARY_FILENAME}', 'w') as f:
        json.dump({
            'summary': all_summary,
            'count': all_count
        }, f, indent=4, separators=(',', ': '))

    print(f'Writing {OUTPUT_DIR}/{ALL_FILES_FILENAME}')
    with open(f'{OUTPUT_DIR}/{ALL_FILES_FILENAME}', 'w') as f:
        json.dump(all_files, f, indent=4, separators=(',', ': '))

    print(f'Writing {OUTPUT_DIR}/{ALL_FILES_BY_PROJECT_FILENAME}')
    with open(f'{OUTPUT_DIR}/{ALL_FILES_BY_PROJECT_FILENAME}', 'w') as f:
        json.dump(all_files_by_project, f, indent=4, separators=(',', ': '))
