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
2. `python3 spreadsheet_id_mapper <ingest API URL> <list of comma-separated spreadsheet submission UUIDs>`

Example:

`python3 spreadsheet_id_mapper.py https://api.ingest.data.humancellatlas.org 8b5feb5e-9039-4c54-9e79-053e490c141a,668791ed-deec-4470-b23a-9b80fd133e1c`

Mappings will be written to a corresponding .json file `mapping_<submission UUID>.json` 
