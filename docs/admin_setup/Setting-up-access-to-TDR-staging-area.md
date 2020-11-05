---
layout: default
title: Upload service
parent: Admin and Setup
has_children: false
nav_order: 5
---

# Setting up access to TDR staging area

## Using your google account
1. Request for your google account to have access to the GCP buckets used for staging area
1. Install gsutil and login using your google account https://cloud.google.com/storage/docs/gsutil_install#sdk-install

## Use Ingest Exporter's GCP credential
1. Install gsutil https://cloud.google.com/storage/docs/gsutil_install#sdk-install

1. Download GCP credential of the exporter from AWS Secrets
   ```
   TODO
   ```
1. Configure gsutil to use the GCP credentials
   ```
   gcloud auth activate-service-account --key-file KEY_FILE
   ```
1. Access the GCP bucket for TDR staging area
   ```
   $ gsutil ls  gs://broad-dsp-monster-hca-dev-ebi-staging/dev 
   ```