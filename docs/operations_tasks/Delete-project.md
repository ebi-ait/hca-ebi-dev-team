---
layout: default
title: Delete project
parent: Operations tasks
has_children: false
nav_order: 1
---

# Delete project
This procedure is to delete a project from the Ingest database. This will not delete referenced entities that belong to other projects. It will not delete data from the Datastore - please ask the datastore directly if you also need this done.

## Steps
1. Use the [`generate_redaction_manifest.py`](https://github.com/HumanCellAtlas/ingest-client/blob/master/ingest/utils/generate_redaction_manifest.py) script to find the entities that need to be deleted for a project.
2. Delete all the entities by running `curl -X DELETE <url>` on all the URLs. This isn't automatically scripted since we anticipate soon replacing this mechanism with an approach that leverages Ingest Mongo data migrations to remove projects.