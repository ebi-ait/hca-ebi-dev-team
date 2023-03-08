---
layout: default
title: Ingest CI/CD
parent: Admin and Setup
---

NEEDS UPDATING
{: .label .label-red }

# Ingest CI/CD

## Why this document?

This is a document for summarizing Ingest's current continuous integration/deployment processes.
## Continuous Integration

* On each pull request, the code is built and unit tests for that repository run in gitlab.
  * see the gitlab-ci.yml on each repo that links to the [common template](https://github.com/ebi-ait/gitlab-ci-templates/)
* Every day, [Ingest-specific integration tests](https://github.com/HumanCellAtlas/ingest-integration-tests) are [run through Gitlab](https://allspark.dev.data.humancellatlas.org/HumanCellAtlas/ingest-integration-tests/pipelines) for all environments except production.


## Continuous Deployment

Changes are automaticall deployed in the following scenarios:
* to dev environment - Merging a pull request to dev branch
* to staging environment - merging to master branch

Deployment to the prod envoronment is done by triggering the "deploy to prod" job.

# Background Material about gitlab and CI/CD

## Setting up a new repository for CI/CD

[![YouTube: Using GitLab CI/CD pipelines with GitHub repositories](https://img.youtube.com/vi/qgl3F2j-1cI/0.jpg)](https://www.youtube.com/watch?v=qgl3F2j-1cI "YouTube: Using GitLab CI/CD pipelines with GitHub repositories")

[GitLab Docs: Using GitLab CI/CD with a GitHub repository](https://docs.gitlab.com/ee/ci/ci_cd_for_external_repos/github_integration.html)

## References
* [Ingest Service Deployment Via Gitlab](https://docs.google.com/document/d/1Cuaw5DBD1VPqySUv7HqL-zCkM-sklUDzpb67XnmIgd4/edit#heading=h.nrf4ftc4j6su) - More information on deploying components through Gitlab.

