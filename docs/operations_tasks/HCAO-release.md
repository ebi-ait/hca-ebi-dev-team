---
layout: default
title: Releasing HCA Ontology Service
parent: Operations tasks
---

# Releasing new version of HCA Ontology Service
1. Check whether [the tagged version image is in Quay.io](https://quay.io/repository/ebi-ait/ontology?tab=tags)
2. Go to your ingest-kube-deployment local repository
3. Update the ONTOLOGY_REF with the new version in the config of the environment you want to update, e.g: `vi config/environment_<dev|staging|prod>`
4. Source the updated environment config: `source config/environment_<dev|staging|prod>`
5. Select the cluster on your command line: `kubectx ingest-eks-<dev|staging|prod>`
6. `cd apps/`
7. `make deploy-ontology`
8. Redeploy `ingest-validator` to clear ontology cache: `kubectl rollout restart deployment ingest-validator`
9. Make sure the correct image has been deployed: `kubectl get deployment ontology -o yaml | grep image`
1. Update the release notes if you are doing the release on staging (/staging/changelog.md) or production (/production/changelog.md)
12. Commit and push your config and release notes changes into the github repository

Note: The validator is caching some ontology values and should be redeployed (even with no version update) to pick up the updates from the new version of HCA Ontology Service

Run the integration-tests on the dev environment and make sure they all pass:

11. Go to `https://gitlab.ebi.ac.uk/hca/ingest-integration-tests/-/pipelines` and click on the `Run Pipeline` button
12. Select the environment from the `Run for` dropdown list and click on the `Run Pipeline` button.
13. Make sure all tests has passed.
14. Repeat all the above steps for the staging and prod environments

