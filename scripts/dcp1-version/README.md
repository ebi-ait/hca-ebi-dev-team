# Populating firstDcpVersion and dcpVersion of DCP1 metadata

The script `populate_dcp_version.py` fixes the missing `dcpVersion` values in the metadata documents in the Ingest database. It reads `dcp1-metadata.txt.tar.gz`  which is the compressed file that contains the list of all the metadata json files in the DCP1 terra bucket `gs://broad-dsp-monster-hca-prod-ucsc-storage/prod/no-analysis/metadata`.

Please see issue: https://github.com/ebi-ait/dcp-ingest-central/issues/481

## How to build docker image and push to quay.io?

```
$ docker build . -t quay.io/ebi-ait/hca-ebi-dev-team:dcp1-version_20211102.5
$ docker push quay.io/ebi-ait/hca-ebi-dev-team:dcp1-version_20211102.5
```

## How to run inside ingest cluster?

```
kubectl run -it dcp1-version --image=quay.io/ebi-ait/hca-ebi-dev-team:dcp1-version_20211102.5  --restart=Never --rm
```
