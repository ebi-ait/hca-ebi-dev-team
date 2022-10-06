---
layout: default
title: Ingest CI/CD
parent: Admin and Setup
---

NEEDS UPDATING
{: .label .label-red }

# Ingest CI/CD

## Last major update
2022-10-06

## Why this document?

This is a document for summarizing Ingest's current continuous integration/deployment processes.

## Continuous Integration

* On each pull request, the code is built and unit tests for that repository run in gitlab.
* Every day, [Ingest-specific integration tests](https://github.com/ebi-ait/ingest-integration-tests) are [run through Gitlab](https://allspark.dev.data.humancellatlas.org/HumanCellAtlas/ingest-integration-tests/pipelines) for all environments except production.

## Continuous Deployment

Deployment is continuous on the dev environment. Any PR created to the dev branch will have a pipeline in gitlab deploy it to dev.

Deployment to staging and production is done after merge to master by triggering the release and deploy jobs in the gitlab pipeline.

## code organization

- component repo
  - .gitlab-ci.yaml
    - includes template
    - allows customization of process, e.g. compoent specific testing
- ingest-kube-deployment
  - apps
    - directory per componet
      - helm chart
      - deployment descriptors (k8s yamls)
- gitlab-ci-templates
  - .gitlab-ci.yaml
    - ci/cd pipeline definition 
- gitlab runner
  - work directory
    - cloned components
    - cloned ingest-kube-deployment 


## Setting up a new repository for CI/CD

[![YouTube: Using GitLab CI/CD pipelines with GitHub repositories](https://img.youtube.com/vi/qgl3F2j-1cI/0.jpg)](https://www.youtube.com/watch?v=qgl3F2j-1cI "YouTube: Using GitLab CI/CD pipelines with GitHub repositories")

[GitLab Docs: Using GitLab CI/CD with a GitHub repository](https://docs.gitlab.com/ee/ci/ci_cd_for_external_repos/github_integration.html)

## References
* [Ingest Service Deployment Via Gitlab](https://docs.google.com/document/d/1Cuaw5DBD1VPqySUv7HqL-zCkM-sklUDzpb67XnmIgd4/edit#heading=h.nrf4ftc4j6su) - More information on deploying components through Gitlab.

