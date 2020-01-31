# S3 bucket for storing modified loom files for March release

See ticket [here](https://app.zenhub.com/workspaces/ingest-dev-5cfe1cb26482e537cf35e8d1/issues/ebi-ait/hca-ebi-dev-team/54)

An S3 bucket has been created in the EBI AWS acc. Address has been shared with wranglers.

## DSS -> Local (or EC2) -> S3

Running the following will download all project files specified in the `one_organ_datasets` into a tmp local folder, 
then sync it with the given bucket. 

```shell script
python cp-loom-files.py one_organ_datasets <s3_bucket>
```

The following assumes you have installed the AWS CLI. No access key or secret is required as the bucket is public (for now).
## List content of S3 bucket
```shell script
aws s3 ls <s3_bucket>
```

## Copy/replace files in S3 bucket
```shell script
aws s3 cp <file_name> <s3_bucket>
```


