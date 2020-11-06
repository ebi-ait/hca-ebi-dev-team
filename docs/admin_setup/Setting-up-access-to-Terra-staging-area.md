---
layout: default
title: Upload service
parent: Admin and Setup
has_children: false
nav_order: 5
---

# Setting up access to Terra staging area

Ingest submits HCA data to [Terra](https://terra.bio/) staging area which is a bucket in Google Cloud Platform (GCP). The GCP buckets locations are configured in `<env>.yaml` files in [ingest-kube-deployment/apps](https://github.com/ebi-ait/ingest-kube-deployment/tree/master/apps)  
   
## Using your google account
1. Request in [`#dcp-2`](https://humancellatlas.slack.com/archives/C01360XN04S) channel from the Data Import team (contact person is `rarshad@broadinstitute.org`) for your google account to have access to the GCP buckets used for staging area

1. Install gsutil and login using your google account. You could follow instructions from https://cloud.google.com/storage/docs/gsutil_install

## Using Ingest Exporter's GCP service account
1. Install gsutil https://cloud.google.com/storage/docs/gsutil_install

1. Download the Ingest Exporter's GCP service account credentials from AWS Secrets
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