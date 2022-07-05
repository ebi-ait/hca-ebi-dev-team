---
layout: default
title: ingest API
has_children: false
---

# API Browser
The [ingest API browser](https://api.ingest.archive.data.humancellatlas.org/") is a [HAL](https://en.wikipedia.org/wiki/Hypertext_Application_Language)
browser for ingest API. It can be used to navigate the api and call the API. It contains 
documentation and information about the available dats and operations.

# Project Search

## Search projects: 

```apiblueprint
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
