# Add metadata to a submission

This repo contains the `add_metadata.py` and a sample `protocol.json` file. The `add_metadata.py` script uses Ingest API and will allow user to add a metadata to an existing submission.

## Steps
1. Create a file containing the metadata json
e.g. See sample protocol.json file in this repo
```
{
  "content": {
    "describedBy": "https://schema.humancellatlas.org/type/protocol/biomaterial_collection/9.2.0/collection_protocol",
    "schema_type": "protocol",
    "protocol_core": {
      "protocol_id": "new_collection_protocol",
      "protocol_name": "A dummy collection protocol",
      "protocol_description": "A dummy collection protocol description",
      "publication_doi": "10.1101/193219",
      "protocols_io_doi": "10.17504/protocols.io.mgjc3un",
      "document": "my_cool_protocol.pdf"
    },
    "method": {
      "text": "percutaneous kidney biopsy",
      "ontology": "EFO:0009293",
      "ontology_label": "percutaneous kidney biopsy"
    }
  }
}
```
2. Get `TOKEN` and `SUBMISSION_URL` from the browser UI and update the variables TOKEN and SUBMISSION_URL inside the `add_metadata.py` script
3. Install dependencies of the script
```
pip install -r requirements.txt
```
3. Run the `add_metadata.py` script
```
python add_metadata.py type filename
```
e.g.
```
python add_metadata.py protocols protocol.json
```

