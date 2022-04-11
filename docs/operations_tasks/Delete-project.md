---
layout: default
title: Delete project
parent: Operations tasks
---

# Delete project
This procedure is to delete an exported project/submission from Ingest database.
If the project was submitted to DCP or EMBL-EBI archives, you should coordinate with them the deletion of that project.

## Steps

1. Delete the exported files from Terra staging area. Please see the SOP on [Setting up access to Terra staging area](../admin_setup/Setting-up-access-to-Terra-staging-area.md) to setup your access.

   This can be done using the following command after setting up Terra access.

   ```
   gsutil -m rm -r gs://broad-dsp-monster-hca-prod-ebi-storage/prod/<project-uuid>
   ```
   
   If the project has already been imported to a Terra dataset, you should coordinate the deletion with Data Import team led by jkorte@broadinstitute.org in the [dcp-2 channel in HCA slack workspace](https://embl-ebi-ait.slack.com/archives/C01360XN04S)

1. Delete the spreadsheet from the broker pod from this location: `/data/spreadsheets/<submission-uuid>` 

   ```
   kubectl get pods | grep broker # get broker pod name
   kubectl exec -i -t <broker-pod-name>  -- /bin/bash
   cd /data/spreadsheets/<submission-uuid>
   rm -r /data/spreadsheets/<submission-uuid>
   ```

1. Delete the submission via UI or API
   When a submission is deleted the upload area will be automatically deleted. This is being done by the ingest-staging-manager deployment.

   It should be possible to delete the submission via UI or the API if the submission state is Pending | Draft | Valid | Invalid. 
   
   via UI:
   There should be a trash bin icon button next to the submission row in the ALL SUBMISSIONS dashboard page.
   Clicking the button will trigger the deletion of the submission.

   via API:
   ```
   export TOKEN='token'
   curl -X DELETE -H "Authorization: Bearer $TOKEN"  https://api.ingest.archive.data.humancellatlas.org/submissionEnvelopes/<object-id>
   ```

   If submission state is already submitted, the only way to delete it is via API with force flag set. 
   ```
   export TOKEN='token'
   curl -X DELETE -H "Authorization: Bearer $TOKEN"  https://api.ingest.archive.data.humancellatlas.org/submissionEnvelopes/<object-id>?force=true
   ```

1. Delete the project in Ingest. All submissions related to the project must be deleted first.
   
   a. It could be deleted via delete button from the UI
   
   b. Or by doing the following command.

   ```
   curl -X DELETE -H "Authorization: Bearer $TOKEN"  https://api.ingest.archive.data.humancellatlas.org/projects/<object-id>
   ```

