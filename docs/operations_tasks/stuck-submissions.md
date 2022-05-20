---
layout: default
title: Investigate Stuck Submissions
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
    ```
    curl -X PUT -H "Authorization: Bearer $TOKEN" https://api.ingest.archive.data.humancellatlas.org/files/<fileDocumentId>/validEvent
    ```

Further investigation needed
- to understand what is happening
- places to look: ingest-validator, ingest-state-tracker and ingest-core logs
- upload service - ingest communication
- see [state tracker](https://github.com/ebi-ait/ingest-state-tracking) README for the submission state diagram

## Problem: submission stuck in "Exporting"

### Description: 
- Submissions can encounter errors/issues during exporting. The submission state can get stuck in "Exporting" and there's no way for user to know what's happening.
- see [ticket](https://app.zenhub.com/workspaces/operations-5fa2d8f2df78bb000f7fb2b5/issues/ebi-ait/hca-ebi-wrangler-central/702)
- **Use [stern](https://github.com/stern/stern) or [graphana](https://monitoring.ingest.archive.data.humancellatlas.org/)** to monitor the logs of multiple exporter pods.


### Steps to troubleshoot:
1. Check the ingest-exporter logs to see if there are failed messages in the exporter.  

   Go to your local workspace of [ingest-kube-deployment](https://github.com/ebi-ait/ingest-kube-deployment) Make sure your access to Ingest EKS clusters are setup correctly. Please follow the repo's README.
   ```bash
   cd ingest-kube-deployment
   ```
   
   Initialize config env vars   
   ```bash
   source config/environment_prod.sh
   ```
   
   Tail all exporter logs and check if there's an exporter instance/pod which failed to process the message
   ```bash
   k8tailall ingest-exporter
   ```
   
   If needed, you may want to get all the logs from the exporter. This will save all logs in a file.
   ```bash
   k8logall ingest-exporter
   ```
   Once you get all the logs into a file, you can do some grep commands to check which pod cause the error
   
   
2. Investigate what the cause of the failure is.
   
### Common Exporter Failures and how to solve them

1. Error: There's a failed request to GCP file transfer status.
   Fix: Delete pod, and let a new pod reprocess the failed message
2. Error: A common failure is when an exporter process timed out waiting for the data transfer from GCP.
   Fix: By design, there will always be only one to trigger and wait for the GCP File transfer job to finish. If that process failed, the job status should be checked manually and the exportJob entity `context` property must be patched to indicate that the file transfer has finished for that submission.
   
   To see the export jobs: https://api.ingest.archive.data.humancellatlas.org/submissionEnvelopes/<submission-object-id>/exportJobs
      
   The export job entity must be patched:
   
   ```bash
   ...
   "context": {
      "totalAssayCount": <assay-count>,
      "isDataTransferComplete": true
   },
   ...
   ```
   
   To check the GCP file transfer status, you can use the script [`get_status.py`](https://github.com/ebi-ait/hca-ebi-dev-team/blob/master/scripts/get_gcp_status/get_status.py).
