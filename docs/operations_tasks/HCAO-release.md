---
layout: default
title: Releasing HCA Ontology Service
parent: Operations tasks
---

# Releasing new version of HCA Ontology Service
1. configure your aws credentials
2. create a [personal access token in gitlab](https://gitlab.ebi.ac.uk/-/profile/personal_access_tokens)
  - only necessary if you want the script to run the integration tests on gitlab for you 
3. clone ingest-kube-deployment repo
4. run for dev environment
```bash
cd ./infra
./scripts/deploy_ontology.sh -v $ONTOLOGY_VERSION -e dev -g $GITLAB_TOKEN
```
5. check integration tests are successful
6. repeat steps 3-4 for staging and prod
```bash
cd ./infra
./scripts/deploy_ontology.sh -v $ONTOLOGY_VERSION -e staging -g $GITLAB_TOKEN
./scripts/deploy_ontology.sh -v $ONTOLOGY_VERSION -e prod -g $GITLAB_TOKEN
7. update status of new ontology ticket on the Ops board.
```

