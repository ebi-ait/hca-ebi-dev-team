---
layout: default
title: Upload service
parent: Admin and Setup
has_children: false
nav_order: 5
---

# Setting up access to TDR staging area

1. Install gsutil https://cloud.google.com/storage/docs/gsutil_install#sdk-install

1. Download GCP credential of the exporter from AWS Secrets

1. Configure gsutil to use the GCP credentials
   ```
       gcloud auth activate-service-account --key-file KEY_FILE
   ```
1. Access the GCP bucket for TDR staging area
   ```
      $ gsutil ls  gs://broad-dsp-monster-hca-dev-ebi-staging/dev 
   ```