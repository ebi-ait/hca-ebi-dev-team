# Fixing and archiving AdultLungElo
This directory contains scripts use for fixing and archiving AdultLungElo submission.
See steps documented: https://docs.google.com/document/d/1jSO4ZvoVlmvuJRJgZ87P1NWMUEzJR7RSn25RNze949g/edit#
See related ticket: https://github.com/ebi-ait/hca-ebi-wrangler-central/issues/724

1. Update the script with token etc and run:
```bash
python `correct_linking.py`
```

2. Update the script to include process uuids to exclude:
```bash
python `remove_bundle_manifests.py`
```