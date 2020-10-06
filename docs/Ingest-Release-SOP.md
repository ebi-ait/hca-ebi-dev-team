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
* Quay.IO will automatically build images for tagged commits, so they can be deployed to any of our environments.
   * You could use the [git release tool](https://github.com/rdgoite/hca-developer-tools/blob/master/gitconfig)
   * You can also just tag builds manually

### Merging to master
1. Create feature branch based from master
2. Tag and deploy the feature branch to dev
   * Coordinate with other devs for using the shared server.
   * Get wrangler feedback during development
3. Create a PR against master
   * Indicate the ZenHub ticket (If no related Zenhub ticket, make this explicit in the PR)
   * Ensure Tests Passing
      * Unit Tests
      * Per-Component Tests
      * End-to-End Tests
   * Requires 1-2 reviewers approval
   * Code coverage should not go down
4. After merge. Tag the merge commit.
5. Deploy the tagged image to Dev.
6. Make sure all tests are passing (unit, ingest integration/e2e tests).
   * Merges that result in failed End-To-End tests should be fixed in `30 minutes`.
   * Developers should collaborate to fix the issue if possible or make the decision to roll back.
7. Release to Staging

### Releasing to staging and prod
1. Coordinate with wranglers who may be using the server
   * Give a heads up during stand up meeting.
2. Update changelog.
   * If we have some extra instructions for deployment, we could note it in the changelog (not really sure where to put this).
3. Deploy tagged master branch
4. Check for failed end-to-end tests
5. Wrangler acceptance testing
6. For production release, add version tag dYYYY-MM-DD.<release-count> (e.g. d2020-03-08.1).
   * If there were 2 releases for that day, the second tag will be d2020-03-08.2
7. Send message to AIT channel #hca when
   * release is starting
   * release is completed + release notes

#### Release schedule
* Staging Release : 10am every tues before sprint demo
* Prod Release : 10am every tues mid sprint

**Adhoc releases can happen and must be agreed upon by the team.**

### Releasing hotfixes
1. Inform the team of the hotfix. Team will decide if hotfix is needed and safe.
2. Branch from the commit hash currently deployed in staging.
3. Tag the commit. Deploy to staging. All tests must passed (DCP tests in staging, ingest tests, unit tests)
5. Make a hotfix release notes
7. Deploy to prod. Make sure all tests passed after hotfix release.

### Links
* [Ingest Integration Tests](https://gitlab.ebi.ac.uk/hca/ingest-integration-tests)
* [CI/CD Plans](https://docs.google.com/document/d/14BdwS44lLNb1Nqxw3Xf6GZlUb4XWkg1Tp8wPs-gFoG4/edit#)