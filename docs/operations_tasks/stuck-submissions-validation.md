---
layout: default
title: Investigate Submissions Stuck in Validation
parent: Operations tasks
---

## Problem: submission stuck in "Metadata Validating"

### Description:
- wranglers have encountered a few cases of submission being stuck in the "metadata validating" state for hours blocking them to export the submission. 
- see [ticket](https://app.zenhub.com/workspaces/operations-5fa2d8f2df78bb000f7fb2b5/issues/ebi-ait/hca-ebi-wrangler-central/702)


### Steps to troubleshoot:
1. Find which entities are in validating
    - in ingest UI, filter each of the biomaterials, processes, protocols and data tabs by "validating"
    - this should pin down which specific entities are stuck
    - in this case, one or more file entities are stuck

1. Check the file validation job status
    - the `validationJob` property will tell if the file validation has completed and successful or not
    - in this case, the `jobCompleted` remained false 

1. Check the AWS batch job for the file
    - check the queue `dcp-upload-validation-q-<env>` for any FAILED job
    - use the Advanced filters to locate the job: 
    - Filter type `Job name`, Filter value `validation-<env>-<sub-uuid>-<validationId>` 
    - for e.g. `validation-prod-9b984263-527f-4fcd-a5a1-c59cd1b91aa3-d8ffa2a0-8747-40cd-8c8a-ff83c3eaa969`
    - check the job validation log for any issue
    - in this case, the validation succeeded

Possible cause:
- file stuck in validating, AWS batch job succeeded, but ingest file document `validationJob` status is not updated which suggests that the upload service call to ingest is sometimes failing / ingest is not receiving and processing the status and set the document to Valid.

Temporary resolution:
- since the file validation succeeded, it should be safe to manually set the file to Valid to unblock the submission
- 
    ```shell
    curl -X PUT -H "Authorization: Bearer $TOKEN" https://api.ingest.archive.data.humancellatlas.org/files/<fileDocumentId>/validEvent
    ```

Further investigation needed
- to understand what is happening
- places to look: ingest-validator, ingest-state-tracker and ingest-core logs
- upload service - ingest communication
- see [state tracker](https://github.com/ebi-ait/ingest-state-tracking) README for the submission state diagram
