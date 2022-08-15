# HCA Ingest Dev Team
Repository for hca ebi dev team agile management. See [zenhub board](https://app.zenhub.com/workspaces/operations-5fa2d8f2df78bb000f7fb2b5/board?repos=232300832,261790554).

## Development Environment Setup

clone this repo and run the makefile to set up everything needed for an 
ingest development  development

```shell
# configure where you store cloned repos
export CLONE_ROOT=/home/$USER/dev
make all
```

## Ingest Documentation 

See [docs/readme.md](docs/readme.md)


## one-off scripts
Any one-off scripts that doesn't have a dedicated location should be maintained in the [scripts](scripts/) directory. See the [readme file](scripts/readme.md) for more instructions.
