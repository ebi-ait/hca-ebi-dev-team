---
layout: default
title: Releasing HCA Ontology Service
parent: Operations tasks
---

# Releasing new version of HCA Ontology Service
1. Check if tagged version image is in Quay.io https://quay.io/repository/humancellatlas/ontology?tab=tags
1. Update the ONTOLOGY_REF with the new version in the config of the environment you want to update, such as https://github.com/ebi-ait/ingest-kube-deployment/blob/master/config/environment_dev
1. [Select the cluster on your command line](https://github.com/HumanCellAtlas/ingest-kube-deployment#accesscreatemodifydestroy-eks-clusters)
1. `cd apps/`
1. `make deploy-app-ontology`
1. `make deploy-app-ingest-validator` Note: The validator is caching some ontology values and should be redeployed with no version update to pick up the updates from the new version of HCA Ontology Service
