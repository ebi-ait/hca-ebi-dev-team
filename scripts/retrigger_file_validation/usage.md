# How to revalidate failed file validation in Ingest

1. Execute the `get_invalid_file_metadata.py` script to create a local file that contains file metadata belongs to the files that failed file validation.
2. Execute `trigger_file_validation.py` script to re-trigger validation of the above files

   This script is doing the following:
   1. Open the list of file resources to be revalidated
   2. Transition state to Invalid temporarily
   3. Set validationJob in file metadata document in ingest to null so that it will trigger a new job
   4. Set the state to DRAFT so that events will be sent again to the validator and validator will trigger validation

3. Go back to the submission in Ingest and monitor the status of the invalid files. 
It depends on the number of invalid files, but after a while all the file's status should be `Valid`.
