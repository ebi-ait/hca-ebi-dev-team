---
layout: default
title: Ingest release process
parent: Operations tasks
---

## Ingest release process 
```
dev
---o--->
   dev-5ddba2b-15-04-2021.1618562812

staging
---o---o---o--->
           staging-5ddba2b-16-04-2021.1618562812

production
---o---o---o---o
               prod-5ddba2b-18-04-2021.1618562812
```


### Pushing changes from dev, through staging, into production
1. Create feature branch based from `dev`
2. Commit your changes
3. Create a pull request (PR) to `dev`
4. Ensure unit tests and build steps are passing in [GitLab](https://gitlab.ebi.ac.uk/hca) for the project you're working on
    - These will be reported in the PR UI in Github
5. Get approvals from two other devs on the PR
6. Merge PR
7. Ensure deploy and integration tests in `dev` environment are passed in GitLab for the project
8. Merge `dev` to `master`
    - `git checkout dev && git pull && git checkout master && git pull && git merge dev && git push`
9. Ensure deploy and integration tests in `staging` environment are passed in GitLab for the project
10. Check deployment in [staging](https://staging.contribute.data.humancellatlas.org/) and consult with wranglers for feedback if neccesary
11. Check with the team if it is okay to deploy this feature to production.
12. Deploy what's on `staging` to `prod` via the operations panel in GitLab
    1. Navigate to [GitLab](https://gitlab.ebi.ac.uk/) > `project your're working on` > operations > environments
    2. Click "Deploy to" next to the `staging` environment
    3. In the dropdown, select "Release prod"
    4. Wait for the "Release prod" stage to complete (you can track the progress on the "CI/CD" page)
    5. In the Environments page, select "Deploy to" again and then select the "Deploy prod" task in the dropdown
    6. Track the deployment in the CI/CD page
13. Ensure your changes are live on prod
    - You may used the `kubectl get pods` command to check this
    - Consult with [these docs](https://github.com/ebi-ait/ingest-kube-deployment) for further information on setting up `kubectl`

### Manually deploying without GitLab
You can manually deploy using the `ingest-kube-deployment` repo if GitLab is down and the deployment is urgent. 

**Deploying manually will disable all of the GitLab tracking features so that the Operations > Environments page is no longer functional**

1. Tag the commit you want to deploy with the [git release tool](https://github.com/rdgoite/hca-developer-tools/blob/master/gitconfig).
    - [quay.io](quay.io) will automatically build tagged commits
2. Find the tag of the built image.
    - You will need the full URL e.g. `quay.io/ebi-ait/ingest-core:123abc`
    - Use this in the next step
3. Follow the steps [here](https://github.com/ebi-ait/ingest-kube-deployment#manually-deploy-one-kubernetes-dockerized-applications-to-an-environment-aws) to deploy the built image.

### Details on GitLab pipeline
#### Shared config
All of the projects use [this template](https://github.com/ebi-ait/gitlab-ci-templates/blob/master/build-release-deploy.yml) for their CI pipelines. This template can be customized on a per-project basis if neccesary. In most cases, the only addition needed is to override the `Unit Test` stage to run the project's unit tests.

#### Stages
```
<feature branch> Unit Test -> Build

<dev branch> Unit Test -> Build -> Release dev -> Deploy dev -> Integration dev

<master branch> Unit Test -> Build -> Release staging -> Deploy staging -> Integration staging
                                      Release prod (manual) -> Deploy prod (manual) -> Integration prod
```

Unit tests and build steps are ran on a feature branch when there is an open PR for that branch. A deployment to staging will be done for every commit to master and a deployment to prod must be triggered manually via the GitLab UI.

#### Image releases
The CI/CD pipeline publishes images to [quay.io](https://quay.io/repository/ebi-ait). Images are first tagged with the shortened commit hash and then retagged as `<environment>-<short commit hash>-<date>.<timestamp>` (e.g. `prod-33242e93-16-04-2021.1618577888`) for a release. This tag is what is deployed to the environments.

#### Kubernetes deployments
GitLab is integrated with the kubernetes cluster and you can see the status of the clusters and configure them [here](https://gitlab.ebi.ac.uk/hca/ingest-staging-manager/-/clusters).

Deployments are done in the pipeline by cloning the `ingest-kube-deployment` repo, sourcing the config files to get the replica counts, and deploying via helm.


### Links
- [Ingest Integration Tests](https://gitlab.ebi.ac.uk/hca/ingest-integration-tests)