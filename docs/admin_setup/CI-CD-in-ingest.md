---
layout: default
title: Ingest CI/CD
parent: Admin and Setup
has_children: false
nav_order: 2
---

# Ingest CI/CD

## Last major update
2019-11-04

## Why this document?

This is a document for summarizing Ingest's current continuous integration/deployment processes. It is a work in progress. For future plans and past detail please see the references.

## Continuous Integration

* On each pull request, the code is built and unit tests for that repository run in Travis.
* Every day, [Ingest-specific integration tests](https://github.com/HumanCellAtlas/ingest-integration-tests) are [run through Gitlab](https://allspark.dev.data.humancellatlas.org/HumanCellAtlas/ingest-integration-tests/pipelines) for all environments except production.
* Twice a day, DCP-wide tests (end-to-end tests created jointly by all components) run in [production](https://allspark-prod.data.humancellatlas.org/HumanCellAtlas/dcp/pipelines) and [integration and staging](https://allspark.dev.data.humancellatlas.org/HumanCellAtlas/dcp/pipelines).

## Continuous Deployment

Deployment is currently **not** continuous - a change in code is not automatically deployed to dev or any other environment. 

However, we can [manually trigger deployment by running a Gitlab pipeline](https://docs.google.com/document/d/1Cuaw5DBD1VPqySUv7HqL-zCkM-sklUDzpb67XnmIgd4/edit#heading=h.nrf4ftc4j6su).

## References
* [Ingest Service Deployment Via Gitlab](https://docs.google.com/document/d/1Cuaw5DBD1VPqySUv7HqL-zCkM-sklUDzpb67XnmIgd4/edit#heading=h.nrf4ftc4j6su) - More information on deploying components through Gitlab.

