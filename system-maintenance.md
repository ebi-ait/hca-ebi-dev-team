# System Maintenance


## Backups

The Ingest database is automatically backed up using a Kubernetes cron job that runs at some specific time of the day. This can be calibrated if needed, but it only usually runs once a day (at midnight). It also runs a verification script that checks if the backup files have been created, and sends an alert message when there’s any problem.

Possible tasks:
- Ensure that backups are up to date
- Random sampling of backup to see if verification works correctly
    - Also, test if backup can be restored
- Check the cloud bucket for usage
- Apply limit to how long backups are kept (e.g. 30 days, 2 weeks, etc.)


# Automated Tests
The end-to-end tests for Ingest runs regularly, and are set up to send results through Slack notifications. It’s important for the tests to always pass as they are required to pass before promoting changes further in the deployment pipeline.

Possible tasks:
- Tests run daily, so it’s good to check if things are running as expected
- In case of failure:
    - Investigate root cause
    - Determine solution
    - Consult the development team if tasks need to be delegated


# Deployments
Kubernetes takes care of most deployment concerns, but from time to time, some services can act up without any warning. Ideally, we should set up monitoring and alerting for this, but in the meantime, regular checks can be done. This can be at the start and/or end of the day.


# AWS Usage
At the time of writing, the HCA development team have been given restricted access to the AWS dashboard, and so this might be a bit challenging. However, the idea here is to be able to collect data about some of the resources we’re using to run our infrastructure. 

Possible tasks:
- Check resources used by the Kubernetes clusters across all our deployment environments
- Regular clean up of allocated resources that aren’t being used
- Checking of backup storage
- Checks for the EC2 instance used for wrangling data

# Upload Service
The Upload Service is now in the legacy software territory and it’s good to anticipate for its code to rot either by itself or through its external dependencies. We can either choose to learn it so we can maintain, or replace it with something else. However, in the meantime, it’s necessary for the team to at least be able to set it up and/or tear it down in its current state.

Possible tasks:
- Set aside time for regular maintenance drills (perhaps once every sprint) where the ops team set up and tear down the upload service.
    - Initially this can be done in a separate deployment environment with the goal of being able to do it in production eventually.
- Ensure that tear downs during the drills do not leave behind resources.
    - Update the infrastructure scripts if there are any issues.
