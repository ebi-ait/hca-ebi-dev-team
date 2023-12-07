---
layout: default
title:  How to update GCP credentials of Ingest Exporter to access Terra staging area
parent: Operations tasks
---

# How to update GCP credentials of Ingest Exporter to access Terra staging area

1. update the secret in aws secrets manager

The secrets to update are for each environment `ingest/<env>/secrets`. The relevant entry is
`ingest_exporter_terra_svc_account`. In this entry the entries `private_key_id` and `private_key` 
would require changing. A new value will be periodically communicated by whoever managed the keys. 
Currently it is the Broad.

1. Go to ingest-kube-deployment local repository
```
cd ingest-kube-deployment
```
1. Initialise environment vars config
```
source config/environment_prod
```
1. Go to apps
```
cd apps
```
1. Redeploy secrets 
```
make deploy-secrets
```
sample output:
```
/Library/Developer/CommandLineTools/usr/bin/make set-context
kubectx ingest-eks-prod
Switched to context "ingest-eks-prod".
kubens prod-environment
Context "ingest-eks-prod" modified.
Active namespace is "prod-environment".
./scripts/deploy_secrets
Release "secrets" has been upgraded. Happy Helming!
NAME: secrets
LAST DEPLOYED: Thu Mar 10 16:08:22 2022
NAMESPACE: prod-environment
STATUS: deployed
REVISION: 20
TEST SUITE: None
NOTES:
Ingest secrets powered by helm charts
```
1. Restart exporter.
```
kubectl rollout restart deployment ingest-exporter
```
sample output:
```
deployment.apps/ingest-exporter restarted
```
1. Run integration tests in prod (The ingest-to terra test doesn't run in prod, but it would be nice to run it and be able to delete any test project ) See ticket [ebi-ait/dcp-ingest-central#699](https://github.com/ebi-ait/dcp-ingest-central/issues/699)
