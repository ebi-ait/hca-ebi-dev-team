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

# metadata serach

For each metadata type: biomaterials, files, processes, protocols, projects, it is possible to query to database using:
```
POST /{metadataType}/query
[
    {
        "field": "validationState",
        "operator": "NE",
        "value": "Valid"
    }
]

```
The body should be an array of criteria, e.g.:
```json
    {
        "field": "validationState",
        "operator": "NE",
        "value": "Valid"
    }
```
Operator can be: `NE`, `IS`, `LT`, `LTE`, `GT`, `GTE`, `IN`, `NIN`, `REGEX`
