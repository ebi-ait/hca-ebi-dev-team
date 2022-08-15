# Make file for generating an HCA ingest development environment from scratch

# TODO: install jdk
# TODO: install nvm/node
# TODO: install git/git-secrets
# TODO: install pyenv/python
# TODO: install jetbrains
# TODO: org membership (git org, google groups)
# TODO: build core broker ui and start
# TODO: import prod db to local mongo

PROJECT_NAME=ingest

.DEFAULT: help
.PHONY: help

help: ## print a help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":[^:]*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# configuration variables
CLONE_ROOT ?= $(HOME)/dev
# end of configuration variables

# TODO: any additional repos needed?
REPOS := \
	ingest-archiver \
	ingest-broker \
	ingest-client \
	ingest-core \
	ingest-data-archiver \
	ingest-exporter \
	ingest-file-archiver \
	ingest-graph-validator \
	ingest-integration-tests \
	ingest-kube-deployment \
	ingest-staging-manager \
	ingest-state-tracking \
	ingest-ui \
	ingest-validator

REPO_DIRS := $(addprefix $(CLONE_ROOT)/,$(REPOS))

all: requirements clone-repos check-aws-profile

# checks whether a tool is available on the OS path
check-installed-%:
	@echo "checking for $(*)"
	@if ! hash echo "$(*)"; then \
		echo -e "\nLooks like $(*) is not installed. See readme for instructions.\n";\
		false;\
	fi

check-python: check-installed-python3
		@if ! python3 -c "import sys; major, minor = sys.version_info[0:2];  sys.exit( else 1)"; then \
    		echo -e "\nLooks like Python 3.9 is not installed or active in the current virtualenv\n"; \
    		false; \
    	fi
check-requirements: check-installed-brew
check-requirements: check-installed-docker
check-requirements: check-installed-git
check-requirements: check-installed-python3
check-requirements: check-installed-pip3
check-requirements: check-installed-docker-compose
check-requirements: check-installed-java
check-requirements: check-installed-aws

install-aws:
	curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "/tmp/AWSCLIV2.pkg" \
		&& sudo installer -pkg /tmp/AWSCLIV2.pkg -target /

install-requirements:
	brew bundle


install-git-secrets:
	cd $(CLONE_ROOT) && git clone https://github.com/awslabs/git-secrets.git \
		&& cd git-secrets && sudo make install
	git secrets --register-aws --global
	git secrets --install ~/.git-templates/git-secrets
	git config --global init.templateDir ~/.git-templates/git-secrets

requirements: install-requirements check-requirements ## check all requirements
	@echo "all requirements for $(PROJECT_NAME) found"

$(CLONE_ROOT):
	echo "setting ingest development environment in $(CLONE_ROOT)"
	mkdir -p $(CLONE_ROOT)

$(CLONE_ROOT)/%:
	git clone https://github.com/ebi-ait/$(@F).git $(@)

clone-repos: install-git-secrets $(CLONE_ROOT) $(REPO_DIRS) ## clone all repos from github

aws-profile: requirements ## setup aws profile
	aws configure set region us-east-1 --profile embl-ebi
	aws configure set role_arn arn:aws:iam::871979166454:role/ingest-devops --profile embl-ebi
	aws configure set source_profile ebi --profile embl-ebi
	aws configure set output json --profile embl-ebi
	aws configure set dummy value --profile ebi

check-aws: aws-profile ## check connection to aws
	aws s3 ls

setup-ingest-kube-deployment: requirements check-aws check-tfswitch
	@mkdir -p ~/.kube
	@cd $(CLONE_ROOT)/ingest-kube-deployment \
		&& tfswitch 0.13.5 \
		&& source config/environment_dev

start-core:
	export SPRING_PROFILES_ACTIVE=local \
		&& cd $(CLONE_ROOT)/ingest-core \
		&& ./run_local.sh

