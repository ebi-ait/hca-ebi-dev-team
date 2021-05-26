---
layout: default
title: Delete project
parent: Operations tasks
---

# Delete project
This procedure is to delete an exported project/submission from the Ingest database. If the project was submitted to DCP or EMBL-EBI archives, you should coordinate with them the deletion of that project.

## Steps
1. Delete the exported files in Terra staging area. Please see the SOP on "Setting up access to Terra staging area" to setup your access.
```
gsutil -m rm -r gs://broad-dsp-monster-hca-prod-ebi-storage/prod/<project-uuid>
```
1. If the Delete Upload area button is in the submissions page in the UI. You could delete thru that. Then wait for the submission to be in Complete state before force deleting the submission.
If there is no delete button, the upload area can be manually deleted. The devs & wrangers should have full s3 permissions s3://org-hca-data-archive-upload-prod/<submission-uuid> 

1. Delete /data/spreadsheets/<submission-uuid> from the broker pod

```
kubectl get pods | grep broker # get broker pod name
kubectl exec -it <broker-pod-name>
cd to /data/spreadsheets/<submission-uuid>
rm -r /data/spreadsheets/<submission-uuid>
```
1. Delete the submission
```
TOKEN='token'
curl -X DELETE -H "Authorization: Bearer $TOKEN"  https://api.ingest.archive.data.humancellatlas.org/submissionEnvelopes/<object-id>\?force\=true
```

1. Delete the project in Ingest. All submissions related to the project must be deleted first.
- could be deleted via delete button from the UI or by doing the following command.

```
curl -X DELETE -H "Authorization: Bearer $TOKEN"  https://api.ingest.archive.data.humancellatlas.org/projects/<object-id>
```

