# Ingest Documentation
The files inside  [docs](docs/) are being published at: https://ebi-ait.github.io/hca-ebi-dev-team/

## Run docs locally
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