# Exporting a DCP1 dataset
see ticket ebi-ait/dcp-ingest-central#793
## Fill missing size and fileContentType

This script fixes the file metadata for DCP1 datasets, in which the `size` and `fileContentType` is not filled due to
being old pieces of metadata. This is one of the fixes needed for exporting a DCP1 project, as the `exporter` needs
these 2 fields to generate the file descriptors.

Other fixes that may be needed, not covered in this script, are:
- Setting up checksums (May not actually be needed - Need to check DCP1 project)
- Migrating project schema to >15.0.0 (Done for most projects)

### Before you start

- Install the requirements: `pip3 install -r requirements.txt`

This will install the hca-ingest client. Last tested with v2.4.1.

### How to run

1. Retrieve the project UUID that contains the submission(s) with the problematic files
2. Ensure that the submission is in an editable state: that means, is not in an `intermediate` status such as `Exporting`
3. Run the script:
```
cd scripts/fill_dcp1_file_metadata
python3 fill_dcp1_metadata.py -p <project_uuid> [-d]
```

The script is then going to run, filling out a log that will be called <project_uuid>.log. Please ensure to check the log.
If you are unsure about what will happen, feel free to use the `-d` (dry-run) option, which will do all the steps and log
it but the PUT operations will be skipped (effectively not modifying the Ingest database).

Once the files have been updated, you will probably need to re-start the submission. If you notice that the status of the submisssion
did not update, please follow (if you have the credentials) or ask a developer for help running the script to [restart the submission](https://github.com/ebi-ait/hca-ebi-dev-team/blob/master/scripts/restart-submission/restart-submission.sh),
indicating that you want to set up the submission to either `Graph valid` or `Metadata valid`.

Once that is done, the submission should be ready to be exported! However, please be aware of the following:
1. You need to tick the box to `export only metadata`. DCP1 data files are **NOT AVAILABLE IN INGEST**.
2. Once exported, you need to delete the following:
    - File descriptors
    - File metadata (Including analysis files, if any)
    - Links

To delete these, please follow the steps below

## Deleting non-needed metadata from staging area

### Before you start 

Please make sure you have the following installed and set-up, with the proper credentials:
- gsutil see https://ebi-ait.github.io/hca-ebi-dev-team/admin_setup/Setting-up-access-to-Terra-staging-area.html#using-ingest-exporters-gcp-service-account

### How to

Run the following lines:
```
export PROJECT_UUID=
echo {descriptors,links,metadata/sequence_file,metadata/analysis_file} | xargs -n1 -I{} gsutil -m rm -r gs://broad-dsp-monster-hca-prod-ebi-storage/prod/${PROJECT_UUID}/{}
```

And it should be ready for import!