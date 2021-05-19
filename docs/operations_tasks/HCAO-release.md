---
layout: default
title: Releasing HCA Ontology Service
parent: Operations tasks
---

# Releasing new version of HCA Ontology Service
1. Check if tagged version image is in Quay.io https://quay.io/repository/ebi-ait/ontology?tab=tags
2. Go to your ingest-kube-deployment local repository
3. Update the ONTOLOGY_REF with the new version in the config of the environment you want to update, e.g: `vi config/environment_<dev|staging|prod>`
4. Source the updated environment config: `source config/environment_<dev|staging|prod>`
5. Select the cluster on your command line: `kubectx ingest-eks-<dev|staging|prod>`
6. `cd apps/`
7. `make deploy-ontology`
8. Get the current image of the ingest-validator and redeploy it: `kubectl get deployment ingest-validator -o yaml | grep image`
9. Get the image from the previous line and deploy the ingest-validator using that image: `make deploy-app-ingest-validator image=quay.io/ebi-ait/ingest-validator:<IMAGE-TAG>`

Note: The validator is caching some ontology values and should be redeployed (even with no version update) to pick up the updates from the new version of HCA Ontology Service

10. Run the integration-tests and make sure they all pass
11. Repeat all the above steps for the staging and prod environments
