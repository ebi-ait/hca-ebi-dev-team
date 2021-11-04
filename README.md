# Dev Team
Repository for hca ebi dev team agile management. See [zenhub board](https://app.zenhub.com/workspaces/operations-5fa2d8f2df78bb000f7fb2b5/board?repos=232300832,261790554).

## one-off scripts

Any one-off scripts that doesn't have a dedicated location should be maintained in the [scripts](scripts/) directory. See the [readme file](scripts/readme.md) for more instructions.

## Run docs locally
1. Follow instructions [here](https://jekyllrb.com/docs/installation/) to install prerequisites
2. `gem install jekyll bundler`
3. `gem install just-the-docs`
4. `(cd docs && jekyll serve)`

## testing uml diagram
![your-UML-diagram-name](http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/ebi-ait/hca-ebi-dev-team/doc/poc-plantuml-diagrams/test.iuml)
