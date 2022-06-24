# Fixing and archiving AdultLungElo
This directory contains scripts use for fixing and archiving AdultLungElo submission.
See steps documented: https://docs.google.com/document/d/1jSO4ZvoVlmvuJRJgZ87P1NWMUEzJR7RSn25RNze949g/edit#
See related ticket: https://github.com/ebi-ait/hca-ebi-wrangler-central/issues/724


This directory contains 3 scripts to accomplish the following:
1. to correct linking
```bash
python `correct_linking.py`
```

2. to delete all bundle manifests to resubmit submission for archiving
```bash
python `delete_all_bundle_manifests.py`
```

2. to the script to include process uuids to exclude:
```bash
python `remove_bundle_manifests.py`
```

Note: Update the script with token , ingest_api url , urls or file paths etc.