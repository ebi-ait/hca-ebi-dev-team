# Update OLS
1. Update the ONTOLOGY_REF in the config of the environment you want to update, such as https://github.com/ebi-ait/ingest-kube-deployment/blob/master/config/environment_dev
1. [Select the cluster on your command line](https://github.com/HumanCellAtlas/ingest-kube-deployment#accesscreatemodifydestroy-eks-clusters)
1. `cd apps/`
1. `make deploy-app-ontology`
1. `make deploy-app-ingest-validator`