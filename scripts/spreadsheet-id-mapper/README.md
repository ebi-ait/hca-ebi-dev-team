# Spreadsheet ID-UUID mapping

Given a submission UUID, outputs a mapping of the IDs within the spreadsheet to their UUIDs, e.g:

```json
 {
      "specimen_from_organism" : {
        "<uuid>" : "<spreadsheet_id>",
        ...
        ...
      },
      "sequence_file" : {
        "<uuid>" : "<spreadsheet_id>",
        ...
        ...
      },
      ...
      ...
    }
```

## Installation and running
(requires python3.x)

1. `pip install -r requirements.txt`
2. `python3 spreadsheet_id_mapper.py <ingest API URL> <input file containing array of project uuids>`

Example:

`python3 spreadsheet_id_mapper.py https://api.ingest.archive.data.humancellatlas.org <input filename>`

Mappings will be written to a corresponding .json file `mapping_<project UUID>_<submission UUID>.json` 

Example content of an input file `dcp2_mvp_project_uuids.json`
```
[
  "7027adc6-c9c9-46f3-84ee-9badc3a4f53b",
  "38449aea-70b5-40db-84b3-1e08f32efe34",
  "ad98d3cd-26fb-4ee3-99c9-8a2ab085e737",
  "f2fe82f0-4454-4d84-b416-a885f3121e59",
  "b4a7d12f-6c2f-40a3-9e35-9756997857e3",
  "83f5188e-3bf7-4956-9544-cea4f8997756",
  "42d4f8d4-5422-4b78-adae-e7c3c2ef511c",
  "95f07e6e-6a73-4e1b-a880-c83996b3aa5c",
  "5b5f05b7-2482-468d-b76d-8f68c04a7a47",
  "c41dffbf-ad83-447c-a0e1-13e689d9b258",
  "2ef3655a-973d-4d69-9b41-21fa4041eed7",
  "f48e7c39-cc67-4055-9d79-bc437892840c",
  "c1a9a93d-d9de-4e65-9619-a9cec1052eaa",
  "b176d756-62d8-4933-83a4-8b026380262f",
  "2086eb05-10b9-432b-b7f0-169ccc49d270",
  "455b46e6-d8ea-4611-861e-de720a562ada"
]
```

