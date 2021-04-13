---
layout: default
title: Terra staging area access
parent: Admin and Setup
---


# Setting up access to Terra staging area

Ingest submits HCA data to [Terra](https://terra.bio/) staging area which is a bucket in Google Cloud Platform (GCP). The GCP buckets locations are configured in `<env>.yaml` files in [ingest-kube-deployment/apps](https://github.com/ebi-ait/ingest-kube-deployment/tree/master/apps)  

```
e.g.

For dev environment, find the value of terraBucketName and terraBucketPrefix in the dev.yaml

The Terra staging area GCP bucket location should be in: 

gs://<terraBucketName>/<terraBucketPrefix>

so the actual bucket location is:

gs://broad-dsp-monster-hca-dev-ebi-staging/dev 

```

## Using your Google account

1. Ensure you are in the [dcp-ingest-team google group](https://groups.google.com/a/data.humancellatlas.org/g/ingest-team)
* Everyone in the dcp-ingest-team google group should have read access to the staging bucket
* New members can be added to this group by group owners, currently:
    * Amnon, Tony, Claire, Oihane
  
_It is the group owners' responsibility to ensure this list is kept up to date and that no one who shouldn't have access is in the group. If you notice someone who should no longer have access, please let the group owners know_

2. Install gsutil and login using your google account. You could follow instructions from https://cloud.google.com/storage/docs/gsutil_install

## Using Ingest Exporter's GCP service account
1. Install gsutil https://cloud.google.com/storage/docs/gsutil_install

1. Download the Ingest Exporter's GCP service account credentials from AWS Secrets. Currently, only Ingest Developers have access to this secret.
   ```
   aws secretsmanager get-secret-value \
    --profile=embl-ebi \
    --region us-east-1 \
    --secret-id ingest/dev/secrets \
    --query SecretString \
    --output text | jq -jr '.ingest_exporter_terra_svc_account' > any-secured-directory/terra-gcp-credentials-dev.json
   ```
   
   Currently, only Ingest developers have access to this secret.
   
1. Configure gsutil to use the GCP credentials
   ```
   gcloud auth activate-service-account --key-file KEY_FILE
   ```
1. Access the GCP bucket for TDR staging area
   ```
   $ gsutil ls  gs://broad-dsp-monster-hca-dev-ebi-staging/dev 
   ```
