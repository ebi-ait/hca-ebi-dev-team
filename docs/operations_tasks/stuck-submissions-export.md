---
layout: default
title: Investigate Submissions Stuck in Exporting
parent: Investigate Stuck Submissions
---

## Problem: submission stuck in "Exporting"

### Description: 
- Submissions can encounter errors/issues during exporting. The submission state can get stuck in "Exporting" and there's no way for user to know what's happening.
- see [ticket](https://app.zenhub.com/workspaces/operations-5fa2d8f2df78bb000f7fb2b5/issues/ebi-ait/hca-ebi-wrangler-central/702)

### Steps to troubleshoot:
0. Go to your local workspace of [ingest-kube-deployment](https://github.com/ebi-ait/ingest-kube-deployment)
    - Make sure your access to Ingest EKS clusters are setup correctly. Please follow the repo's README.
1. Errored export messages should now be added to the Error Queue for invesitgation
    -  `ingest.exporter.errored.queue`
    ```bash
    cd ingest-kube-deployment
    source config/environment_prod
    kubectl port-forward rabbit-0 15672:15672
    ```
    - [Rabbit Management Console](localhost:15672/#/queues/)
    - View the messages in the queue **without acknowledging them** to give you id's that you can use in your log investigation
    - If the errors are due to temporary problems you can move the messages back to their original queue to be reprocessed.
    - *More information will be added here as we use this diagnostic path*
2. Check the ingest-exporter logs to see if there are failed messages in the exporter.
    - using [stern](https://github.com/stern/stern)
    ```bash
    cd ingest-kube-deployment
    source config/environment_prod
    stern ingest-exporter
    ```
    - or [graphana](https://monitoring.ingest.archive.data.humancellatlas.org/)
        - usefull query: `{container=~"ingest-.*"} |= "<submission-uuid>"` 
3. Investigate what the cause of the failure is.
4. Check whether Submission is Actually Exported
    1. count metadata by type on the staging area
    ```shell
    gsutil ls -r gs://broad-dsp-monster-hca-prod-ebi-storage/prod/<project-uuid>/metadata | grep -v /: | cut -d/ -f7 | sed -r '/^\s*$/d' | uniq -c | sort -k2,2
    ```
    2. compare to ingest api:
    ```
    curl https://api.ingest.archive.data.humancellatlas.org/submissionEnvelopes/<submission_id>/submissionManifest
    ```
    3. Check whether Required Changes are visible in the Staging Area
    4. Check the entities you know were supposed to change.
    
### Common Exporter Failures and how to solve them

#### Error: There's a failed request to GCP file transfer status.

Fix: Delete pod, and let a new pod reprocess the failed message

#### Error: A common failure is when an exporter process timed out waiting for the data transfer from GCP.

Fix: By design, there will always be only one to trigger and wait for the GCP File transfer job to finish. If that process failed, the job status should be checked manually and the exportJob entity `context` property must be patched to indicate that the file transfer has finished for that submission.
   
   To see the export jobs: `https://api.ingest.archive.data.humancellatlas.org/submissionEnvelopes/<submission-object-id>/exportJobs`
      
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
