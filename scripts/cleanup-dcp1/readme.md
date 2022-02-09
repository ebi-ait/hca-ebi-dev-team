# Cleanup DCP1 projects
This script cleans any the terra staging area of DCP1 projects so that they are ready to export again if changes have been made

**You need to have gsutil setup with the correct credentials prior to running this**

## Instructions
1. `pip install -r requirements.txt`
2. Get an ingest token and add it to your env vars as `INGEST_API_TOKEN`
3. Fill in `submissions_uuids.txt` with submission UUIDs you want to process on each line
4. `python ./cleanup.py`
5. Any skipped submissions will be put in `skipped_terra_fixes.csv`