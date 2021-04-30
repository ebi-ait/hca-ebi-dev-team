---
layout: default
title: Retry failed ingest exporter
parent: Operations tasks
---

# How to retry failed experiments in the Ingest Exporter

If a submission got stuck in `Processing` state, it's possible that there are some experiments that failed to export.
Determine the cause of failure. After fixing it, exporting can be triggered again by redeploying exporter.

## Via the GitLab UI (recommended)
Go [here](https://gitlab.ebi.ac.uk/hca/ingest-exporter/-/environments) and click the "re-deploy to environment" button next to the environment that has stuck submissions.

## Via `ingest-kube-deployment` (not recommended)
If GitLab is down and it is urgent to redeploy, you can do this manually. 

**Doing this will disable GitLab environment tracking features. This should not be done without approval from a consortium of devs.**

1. Go to [quay.io](https://quay.io/repository/ebi-ait/ingest-exporter?tab=tags)
2. Find the tag that is currently deployed to the environment of concern
    - e.g. `prod-4bfa2e0f-16-04-2021.1618562812`
    - The second part of the tag is the commit hash so check in Git what the latest commit hash is on the branch (`master` for prod and staging environments, `dev` for dev environment) and use that tag
3. Go to your locally cloned `ingest-kube-deployment` repo
4. `source config/environment_<dev/staging/prod>`
5. `cd apps`
6. `make deploy-app-ingest-exporter image=quay.io/ebi-ait/ingest-exporter:<tag>`
    - e.g. `make deploy-app-ingest-exporter image=quay.io/ebi-ait/ingest-exporter:prod-4bfa2e0f-16-04-2021.1618562812`
