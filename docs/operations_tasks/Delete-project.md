---
layout: default
title: Delete project
parent: Operations tasks
---

# Delete project
This procedure is to delete an exported project/submission from Ingest database.
If the project was submitted to DCP or EMBL-EBI archives, you should coordinate with them the deletion of that project.

## Steps
1. Delete the submission upload area in Ingest.

   If the _Delete Upload area_ button appears in the submissions page in the UI. You can click on it to delete the upload area. 
   
   The upload area can be deleted from the AWS console or hca-util using the `delete` command with the `-d` flag (with the wrangler access key).

      
   The devs & wranglers should have full s3 permissions on `s3://org-hca-data-archive-upload-prod/<submission-uuid>`

2. Delete the exported files from Terra staging area. Please see the SOP on [Setting up access to Terra staging area](../admin_setup/Setting-up-access-to-Terra-staging-area.md) to setup your access.

   This can be done using the following command after setting up Terra access.

   ```
   gsutil -m rm -r gs://broad-dsp-monster-hca-prod-ebi-storage/prod/<project-uuid>
   ```

3. Delete the spreadsheet from the broker pod from this location: `/data/spreadsheets/<submission-uuid>` 

   ```
   kubectl get pods | grep broker # get broker pod name
   kubectl exec -i -t <broker-pod-name>  -- /bin/bash
   cd /data/spreadsheets/<submission-uuid>
   rm -r /data/spreadsheets/<submission-uuid>
   ```

4. Delete the submission
   
   **Note**: You have to wait for the submission to be in Complete state before force deleting the submission.

   ```
   export TOKEN='token'
   curl -X DELETE -H "Authorization: Bearer $TOKEN"  https://api.ingest.archive.data.humancellatlas.org/submissionEnvelopes/<object-id>?force=true
   ```

5. Delete the project in Ingest. All submissions related to the project must be deleted first.
   
   a. It could be deleted via delete button from the UI
   
   b. Or by doing the following command.

   ```
   curl -X DELETE -H "Authorization: Bearer $TOKEN"  https://api.ingest.archive.data.humancellatlas.org/projects/<object-id>
   ```

