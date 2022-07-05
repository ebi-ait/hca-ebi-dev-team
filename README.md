# HCA Ingest Dev Team
Repository for hca ebi dev team agile management. See [zenhub board](https://app.zenhub.com/workspaces/operations-5fa2d8f2df78bb000f7fb2b5/board?repos=232300832,261790554).


## Ingest Documentation 
The files inside  [docs](docs/) are being published at: https://ebi-ait.github.io/hca-ebi-dev-team/

### Run docs locally
1. Follow instructions [here](https://jekyllrb.com/docs/installation/) to install prerequisites
2. install the ruby bundle 
```shell
bundle install
```

3. serve the docs
```shell
cd docs
bundle exec jekyll serve -c _config_local.yml
```



## one-off scripts
Any one-off scripts that doesn't have a dedicated location should be maintained in the [scripts](scripts/) directory. See the [readme file](scripts/readme.md) for more instructions.
