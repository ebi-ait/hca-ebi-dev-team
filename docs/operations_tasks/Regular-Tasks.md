---
layout: default
title: Regular Tasks Checklist
parent: Operations tasks
---

NEEDS UPDATING
{: .label .label-red }

Please see the [google sheet](https://docs.google.com/spreadsheets/d/1uUOWdthsXutBLhiax_mRs8mQ6UA3Zkr07jWdlqBrB1Q/edit#gid=0) to view/record when each task was performed.


## Backups
The Ingest database is automatically backed up using a Kubernetes cron job that runs at some specific time of the day. This can be calibrated if needed, but it only usually runs once a day (at midnight). It also runs a verification script that checks if the backup files have been created, and sends an alert message when there’s any problem.

Backups are located in the [`ingest-db-backup`](https://s3.console.aws.amazon.com/s3/buckets/ingest-db-backup?region=us-east-1) S3 bucket and any objects are deleted after 90 days.

### Tasks
- Ensure backups are up to date (**once per fortnight**)
    - Check that there is an object (`*.tar.gz`) file for today's backup in `dev`, `staging`, and `prod`.
- Random sampling of backup to see if verification works correctly and test it can be restored (**once per month**)
    1. Download a randomly selected backup from one of the environments (check it's not the same one listed in **extra notes** in the spreadsheet)
    2. untar it: `tar -xzvf 2020-12-15T00_00.tar`
    3. Spin up a docker container: `docker run -d --name test-mongo -v $PWD/data/db:/data/db mongo:latest`
    4. Connect to it: `docker exec -it test-mongo /bin/bash`
    5. Restore from backup: `mongorestore /data/db/dump/BACKUP_FOLDER/`
    6. Connect to mongo: `mongo`
    7. Use admin: `use admin`
    8. Run each of these and ensure count seem sensible: `db.biomaterial.count()`, `db.bundleManifest.count()`, `db.file.count()`, `db.process.count()`, `db.project.count()`, `db.protocol.count()`, `db.submissionEnvelope.count()`
    9. `exit`
    10. `exit`
    11. `docker stop test-mongo && docker rm test-mongo && rm -rf <BACKUP_FILE>.tar`
    12. Take note of the backup file tested in the spreadsheet
- Check the cloud bucket for active usage [here](https://s3.console.aws.amazon.com/s3/bucket/ingest-db-backup/metrics/bucket_metrics?region=us-east-1&tab=storage&period=2w) (**once per month**)

## Deployments
Kubernetes takes care of most deployment concerns, but from time to time, some services can act up without any warning. Ideally, we should set up monitoring and alerting for this, but in the meantime, regular checks can be done. This can be at the start and/or end of the day.

Use `kubectl get pods`
and `kubectl get pods -n kube-system`

### Tasks
- Check all pods running (**daily**)

## End-to-end tests
Some manual e2e tests are currently documented [here](e2e-tests.html). These do not need to run reguarly but should be run whenever major changes occur.


## AWS Usage
Some tasks to collect data about some of the resources we're using to run or infrastructure. [Cloudwatch](https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#cw:dashboard=Overview) can be used to monitor.

### Tasks
- Monitor resource usage with Cloudwatch (**once per month**)
- Clean up of unused allocated resources (**once per month**)

## Upload Service
The Upload Service is now in the legacy software territory and it’s good to anticipate for its code to rot either by itself or through its external dependencies. We can either choose to learn it so we can maintain, or replace it with something else. However, in the meantime, it’s necessary for the team to at least be able to set it up and/or tear it down in its current state.

## Tasks:
- Set up and tear down the upload service (**once per sprint**)
    - Just do in dev or staging
    - Ensure that tear downs during the drills do not leave behind resources.
    - Update the infrastructure scripts if there are any issues.

