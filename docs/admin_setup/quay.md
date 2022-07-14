# Quay.io
## A bunch of important stuff
To Do: Write about this stuff

## Maintaining ingest_base_images
### Adding an image

```bash
docker login quay.io
docker pull <image>:<tag>
docker tag <image>:<tag> quay.io/ebi-ait/ingest-base-images:<image>_<tag>
docker push quay.io/ebi-ait/ingest-base-images:<image>_<tag>
```
Example
```bash
docker pull python:3.10-slim
docker tag python:3.10-slim quay.io/ebi-ait/ingest-base-images:python_3.10-slim
docker push quay.io/ebi-ait/ingest-base-images:python_3.10-slim
```
