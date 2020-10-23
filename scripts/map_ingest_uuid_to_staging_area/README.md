# Map UUIDs from ingest to files in the staging area

Given a list of files from the staging area and the output from another tool from this repository ([spreadsheet ID mapper](/scripts/spreadsheet-id-mapper/src/spreadsheet_id_mapper.py)), return a mapping of the different entities in ingest to the files in the staging area.

## pre-requisites

1. [gsutil](https://cloud.google.com/storage/docs/gsutil_install) tool
1. python=>3.6
1. Configure gsutil to be able to do operations on the staging area (Contact a dev for that)
1. [spreadsheet ID mapper](/scripts/spreadsheet-id-mapper/src/spreadsheet_id_mapper.py) requirements

## How to run

### Before running

1. Run the following command to obtain a list of files from the staging area:
   ```
   gsutil ls -lr gs://broad-dsp-monster-hca-prod-ebi-storage/prod/ | awk '{if($3 != "")print $3}' > all_files.txt
   ```
   This command will retrieve all the files and folders below `prod/`. Awk processing to delete folders from this list
   
1. Run the spreadsheet ID mapper to obtain a map of the UUIDs for ingest entities based on the submission uuid.
   
   <span style="color: red">**NOTE**</span>: Sometimes the mapper does not retrieve the project UUID. Please check and add it manually if needed.
   
### Running

1. Run the following command:
    ```
    python3 map_uuids_to_staging_area <path_to_uuid_mapping> <path_to_staging_area_file_list>
    ```
1. You will get an output with a similar layout as the output from the spreadsheet ID mapper, but with the IDs replaced with the staging area path.
   
   <span style="color: red">**NOTE**</span>: If there is no match in the staging area, the ID will be preserved. This can be used to check if a project is indeed in the staging area!
   
