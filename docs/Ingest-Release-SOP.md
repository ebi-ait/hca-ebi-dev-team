# Ingest SOP's

## Ingest release process 
```
dev
---o--->
   5ddba2b

staging
---o---o---o--->
           5ddba2b

production
---o---o---o---o
               5ddba2b, d2020-03-08.1
```

### Tagging latest commits
Quay.IO will automatically build images for tagged commits, so they can be deployed to any of our environments.
* You could use the [git release tool](https://github.com/rdgoite/hca-developer-tools/blob/master/gitconfig)
* You can also just tag builds manually

### Merging to master
1. Create feature branch based from master
1. Tag and deploy the feature branch to dev
> Note: You will need to coordinate with other users as it is a shared environment.
- You may do this for many reasons, including:
    - Manual testing of microservices interactions
    - Running automated end-to-end tests
    - Getting wrangler feedback during development if needed
3. Create a PR against master
    - Indicate the ZenHub ticket (If no related Zenhub ticket, make this explicit in the PR)
    - Ensure Tests Passing
        - Unit Tests
        - Per-Component Tests
        - End-to-End Tests
    - Requires 1-2 reviewers approval
    - Code coverage should not go down
1. Merge to master.
1. After merge. Tag the merge commit.
1. Deploy the tagged image to Dev.
1. Make sure all tests are passing (unit, ingest integration/e2e tests).
    - Merges that result in failed End-To-End tests should be fixed in `30 minutes`.
    - Developers should collaborate to fix the issue if possible or make the decision to roll back.
1. Release to Staging

### Releasing to staging and prod
1. Coordinate with wranglers who may be using the server
    - Give a heads up during stand up meeting.
1. Copy the `staging` deployment to `production` by copying respective staging environment image tags to production.
1. Update changelog.
    - Copy the staging changelog from since the last production release date and merge changelog entries for the various components
    - If we have some extra instructions for deployment, we could note it in the changelog (not really sure where to put this).
1. Deploy the new production deployment configuration
1. Check for failed end-to-end tests
1. Wrangler acceptance testing
1. For production release, add version tag dYYYY-MM-DD.<release-count> (e.g. d2020-03-08.1) in quay.io.
    - If there were 2 releases for that day, the second tag will be d2020-03-08.2
    - (Optional) Comment inline these version tag in the production deployment configuration
1. Send message to AIT channel #hca when
    - release is starting
    - release is completed + release notes

#### Release schedule
- Staging Release : 10am every tues before sprint demo
- Prod Release : 10am every tues mid sprint

**Adhoc releases can happen and must be agreed upon by the team.**

### Releasing hotfixes
1. Inform the team of the hotfix. Team will decide if hotfix is needed and safe.
1. Branch from the commit hash currently deployed in staging.
1. Tag the commit. Deploy to staging. All tests must passed (DCP tests in staging, ingest tests, unit tests)
1. Make a hotfix release notes
1. Deploy to prod. Make sure all tests passed after hotfix release.

### Links
- [Ingest Integration Tests](https://gitlab.ebi.ac.uk/hca/ingest-integration-tests)
- [CI/CD Plans](https://docs.google.com/document/d/14BdwS44lLNb1Nqxw3Xf6GZlUb4XWkg1Tp8wPs-gFoG4/edit#)
