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

`python3 spreadsheet_id_mapper.py https://api.ingest.data.humancellatlas.org <input filename>`

Mappings will be written to a corresponding .json file `mapping_<project UUID>_<submission UUID>.json` 
