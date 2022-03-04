# How to revalidate failed file validation in Ingest

1. Get the JWT Token from Ingest UI and place it into the `trigger_file_validation` script replacing the value of the `TOKEN` variable
2. Get the ID of the `submissionEnvelope` you would like to work with and place it into the `trigger_file_validation` script replacing the `id` (`replace_with_id`) in the `SUBMISSION_URL` variable
3. Execute the `get_invalid_file_metadata.py` script to create a local file that contains file metadata belongs to the files that failed file validation.
4. Execute `trigger_file_validation.py` script to re-trigger validation of the above files

   This script is doing the following:
   1. Open the list of file resources to be revalidated
   2. Transition state to Invalid temporarily
   3. Set validationJob in file metadata document in ingest to null so that it will trigger a new job
   4. Set the state to DRAFT so that events will be sent again to the validator and validator will trigger validation

5. Go back to the submission in Ingest and monitor the status of the invalid files. 
It depends on the number of invalid files, but after a while all the file's status should be `Valid`.
