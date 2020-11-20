---
layout: default
title: Manual Steps for Unpublishing schemas
parent: Operations tasks
---

# Manual Steps for Unpublishing schemas
1. Remove the schema from the schema bucket `schema.dev.archive.data.humancellatlas.org`
2. Delete the schema entry from Ingest database 
```
db.schema.deleteOne({"highLevelEntity": "type", "domainEntity": "project", "schemaVersion": "15.0.0"});
```
