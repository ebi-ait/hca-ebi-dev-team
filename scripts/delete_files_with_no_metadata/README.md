# Delete files with no metadata
 Fixes a submission which has data files uploaded/synced to the Ingest submission upload area but have no metadata from the spreadsheet. 

## How to run

1. Modify and provide the details in the script 
```
DRY_RUN = False
TOKEN = 'insert-token-without-bearer-prefix'
SUBMISSION_URL = 'https://api.ingest.archive.data.humancellatlas.org/submissionEnvelopes/insert-submission-id'
```

2. Run the script:
```python
python delete_files_with_no_metadata.py
```
