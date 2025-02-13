---
layout: default
title: ingest API
has_children: true
---

# API Browser
The [ingest API browser](https://api.ingest.archive.data.humancellatlas.org/") is a [HAL](https://en.wikipedia.org/wiki/Hypertext_Application_Language)
browser for ingest API. It can be used to navigate the api and call the API. It contains 
basic documentation and information about the available dats and operations.

# Project Search

## Search projects endpoint: 

```
GET /projects/filter?search={search_keys}
```

query parameters:

| parameter  | description                         | example         |
|:-----------|:------------------------------------|:----------------|
| search     | search keys                         | EGAD00001007718 |
| searchType | AnyKeyword, AllKeywords, ExactMatch | AllKeywords     |
| page       |                                     | 0               |
| size       |                                     | 20              |
| sort       | field name, direction               | updateDate,desc |


## Additional search methods:

```text/vnd.apiblueprint
GET /projects/search
```

# Metadata search

For each metadata type: biomaterials, files, processes, protocols, projects, it is possible to query arbitrarily the database:

```
POST /{metadataType}/query
Authorization: Bearer <TOKEN>

[
    {
        "field": "validationState",
        "operator": "NE",
        "value": "Valid"
    }
]
```

## Available operators
Operator can be: `NE`, `IS`, `LT`, `LTE`, `GT`, `GTE`, `IN`, `NIN`, `REGEX`

## Query Patterns

### querying multiple fields
The body can have a list of comma separated criteria, e.g.:

```json
    [
        {
            "field": "validationState",
            "operator": "NE",
            "value": "Valid"
        },
        {
            "field": "content.process_core.process_id",
            "operator": "IS",
            "value": "my_process"
        },
    ]
```

### Querying Referenced Fields

To query referenced fields use the `.id` after the reference field's name.
For example, to query processes by the submission to which the belong use the following criterion:

```json
{
        "field": "submissionEnvelope.id",
        "operator": "IS",
        "value": "64e36dfba3737b41e55023da"
}
```

### Querying array fields

To find all documents that have a value inside an array, use the following query. In this case, `hca_bionetworks` is the array field and `name` is an attribute of each element in the array. This query is an improvised version of an `exists` query.

```json
[
    {
        "field": "content.hca_bionetworks.name",
        "operator": "REGEX",
        "value": ".*"
    }   
]
```
