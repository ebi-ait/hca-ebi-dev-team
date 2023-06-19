---
layout: default
title: Onboarding
parent: Admin and Setup
---

# Ingest Developer Getting Started
{: .no_toc }


{% include ingest-architecture.md %}

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Access
* create an [ebi account](https://account-manager.ebi.ac.uk/signin)
* github
  * [ebi-ait Github organisation](https://github.com/ebi-ait) (set up 2-factor auth; install secret on machine)
    * Add developer to [hca-dev team](https://github.com/orgs/ebi-ait/teams/hca-dev)
  * [HumanCellAtlas Github organisation](https://github.com/HumanCellAtlas) (set up 2-factor auth; install secret on machine)
* Slack
  * [Slack: HCA](https://humancellatlas.slack.com/)
    * #dcp-2
  * [Slack: AIT](https://embl-ebi-ait.slack.com)
* [EBI GitLab](http://gitlab.ebi.ac.uk/)
* login to [EBI AWS](https://embl-ebi.awsapps.com/start#/)
   1. need to be in Google Group [grp-aws-ait-team-power-users](https://groups.google.com/a/ebi.ac.uk/g/grp-aws-ait-team-power-users/members). If you are not a member, talk to your supervisor.
   2. You can click on ‘Management console’ to access console or use ‘Command line or programmatic access’ to access aws CLI. Add to your profile (`~/.aws/config`, `~/.aws/credentials`):
      * aws_access_key_id=
      * aws_secret_access_key= 
      * aws_session_token=
   3. note: The CLI Keys along with browser login session are short lived and has a timeout of 4hr.
   4. Please reach to [Cloud-consultants](mailto:cloud-consultants@ebi.ac.uk) for any connection problems. 

* [Quay.io](https://quay.io/organization/ebi-ait) - for built docker image storage
* [Confluence](https://www.ebi.ac.uk/seqdb/confluence/display/HCA/Human+Cell+Atlas+Home)
* [Zenhub](https://app.zenhub.com/workspaces/ingest-dev-5cfe1cb26482e537cf35e8d1/board)
* Google Apps (Google Drive [Shared HCA folder](https://drive.google.com/drive/folders/0B-_4IWxXwazQaEh1SnhOOHV4S0k) & Calendar) - use EBI Single sign-on
* [Snyk](https://app.snyk.io/org/humancellatlas/)
* mailing lists:
  * [Ingest group e-mail](https://listserver.ebi.ac.uk/mailman/listinfo/hca-ingest-dev)
  * [ait](https://listserver.ebi.ac.uk/mailman/listinfo/ait)
* Calendar
  * see [Wranglers' onboarding page](https://ebi-ait.github.io/hca-ebi-wrangler-central/ebi-wrangler-onboarding.html#calendar)


# Licenses
## JetBrains Licenses
* IntelliJ IDEA Ultimate - can be used for java/python, node
* Alternatively, the language packs can be used: PyCharm Professional, WebStorm

1. Create a JetBrains Account using @ebi.ac.uk address - [Register here](https://account.jetbrains.com/login)
2. Email: [itsupport@ebi.ac.uk](mailto:itsupport@ebi.ac.uk)
3. Ask for to be included in the “JetBrains All Products Pack”

_Other software uses free/community licensing._

# Software
_Caveat: All practical descriptions for Mac/Linux._
1. [Homebrew](https://brew.sh/)
2. git and git-secrets
3. [Docker Desktop](https://www.docker.com/products/docker-desktop)
4. Kubernetes tools: follow http://github.com/ebi-ait/ingest-kube-deployment
5. docker-machine-driver-hyperkit
```
brew install docker-machine-driver-hyperkit
sudo chown root:wheel /usr/local/opt/docker-machine-driver-hyperkit/bin/docker-machine-driver-hyperkit
sudo chmod u+s /usr/local/opt/docker-machine-driver-hyperkit/bin/docker-machine-driver-hyperkit
```

## MongoDB
Follow the [MongoDB installation guide](https://docs.mongodb.com/manual/installation/) for your platform.

## RabbitMQ
Follow the [RabbitMQ installation guide](https://www.rabbitmq.com/download.html) for your platform.

## Repositories
### Ingest-Core (InteliJ)
see [readme](https://github.com/ebi-ait/ingest-core)
#### Run Dependencies in Docker
```
docker-compose up mongo rabbitmq
```
#### Run Locally
1. Add [Plugin](https://plugins.jetbrains.com/plugin/6317-lombok/) for [Project Lombok](https://projectlombok.org) 
2. Edit Preferences: Preferences | Build, Execution, Deployment | Build Tools | Gradle
    1. Build and run using: **Gradle**
    2. Run tests using: **IntelliJ IDEA**
3. Adjust IntelliJ Configuration
    1. Create the following folder in IntelliJ under ingest-core project: `.idea/runConfigurations`.
    2. Create `.idea/runConfigurations/Ingest_Core_Dependencies.xml`

        ```
        <component name="ProjectRunConfigurationManager">
          <configuration default="false" name="Ingest-Core Dependencies" type="docker-deploy" factoryName="docker-compose.yml" activateToolWindowBeforeRun="false" server-name="Docker">
            <deployment type="docker-compose.yml">
              <settings>
                <option name="envVars">
                  <list>
                    <DockerEnvVarImpl>
                      <option name="name" value="MONGO_URI" />
                      <option name="value" value="mongodb://localhost:27017/admin" />
                    </DockerEnvVarImpl>
                    <DockerEnvVarImpl>
                      <option name="name" value="RABBIT_HOST" />
                      <option name="value" value="localhost" />
                    </DockerEnvVarImpl>
                    <DockerEnvVarImpl>
                      <option name="name" value="RABBIT_PORT" />
                      <option name="value" value="5672" />
                    </DockerEnvVarImpl>
                    <DockerEnvVarImpl>
                      <option name="name" value="SCHEMA_BASE_URI" />
                      <option name="value" value="https://schema.humancellatlas.org/" />
                    </DockerEnvVarImpl>
                  </list>
                </option>
                <option name="services">
                  <list>
                    <option value="mongo" />
                    <option value="rabbitmq" />
                  </list>
                </option>
                <option name="sourceFilePath" value="docker-compose.yml" />
              </settings>
            </deployment>
            <method v="2" />
          </configuration>
        </component>
        ```

    3. Create `.idea/runConfigurations/Ingest_Core_Application.xml`

      ```
<component name="ProjectRunConfigurationManager">
    <configuration default="false" name="Ingest-Core Application" type="SpringBootApplicationConfigurationType" factoryName="Spring Boot">
        <module name="ingest-core.main" />
        <option name="SPRING_BOOT_MAIN_CLASS" value="org.humancellatlas.ingest.IngestCoreApplication" />
        <option name="VM_PARAMETERS" value="-XX:+UseG1GC" />
        <option name="PROGRAM_PARAMETERS" value="--spring.data.mongodb.uri=mongodb://localhost:27017/admin" />
        <option name="ALTERNATIVE_JRE_PATH" />
        <envs>
            <env name="SCHEMA_BASE_URI" value="https://schema.humancellatlas.org/" />
            <env name="AUTH_ISSUER" value="https://login.elixir-czech.org/oidc/" />
            <env name="SVC_AUTH_AUDIENCE" value="https://dev.data.humancellatlas.org/" />
            <env name="USR_AUTH_AUDIENCE" value="https://dev.data.humancellatlas.org/" />
            <env name="GCP_JWK_PROVIDER_BASE_URL" value="https://www.googleapis.com/service_accounts/v1/jwk/" />
            <env name="GCP_PROJECT_WHITELIST" value="hca-dcp-production.iam.gserviceaccount.com,human-cell-atlas-travis-test.iam.gserviceaccount.com,broad-dsde-mint-dev.iam.gserviceaccount.com,broad-dsde-mint-test.iam.gserviceaccount.com,broad-dsde-mint-staging.iam.gserviceaccount.com" />
        </envs>
        <method v="2">
            <option name="Make" enabled="true" />
        </method>
    </configuration>
</component>
      ```

    4. This will set the following environment variables:
      - SCHEMA_BASE_URI=https://schema.humancellatlas.org/
      - GCP_PROJECT_WHITELIST=hca-dcp-production.iam.gserviceaccount.com,human-cell-atlas-travis-test.iam.gserviceaccount.com,broad-dsde-mint-dev.iam.gserviceaccount.com,broad-dsde-mint-test.iam.gserviceaccount.com,broad-dsde-mint-staging.iam.gserviceaccount.com
      - AUTH_ISSUER=https://login.elixir-czech.org/oidc/
      - SVC_AUTH_AUDIENCE=https://dev.data.humancellatlas.org/
      - USR_AUTH_AUDIENCE=https://dev.data.humancellatlas.org/
      - GCP_JWK_PROVIDER_BASE_URL=https://www.googleapis.com/service_accounts/v1/jwk/

    5. Restart your IntelliJ IDEA.

### Ingest-Broker (PyCharm)
#### Run in Docker
```
docker build -t humancellatlas/ingest-broker .
docker-compose up
```
#### Run Locally
Install Python 3.6 or higher
```
brew install pyenv
pyenv install --list
pyenv install 3.7.4 
```
Will return something like:
```
Installed Python-3.7.4 to /Users/<username>/.pyenv/versions/3.7.4
```
Preferences | Project: ingest-broker | Project Interpreter
[[/images/image1.png]]

### Ingest-UI

1. Install NVM
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash
```
2. Add to ~/.bash_profile, Restart Terminal
```
source ~/.bashrc
```
3. Install Node
```
nvm install node@12.16.3
```
4. Install Yarn
```
brew install yarn@1.22.4
```
5. Add to ~/.bashrc, Restart Terminal
```
export PATH="$PATH:/usr/local/Cellar/yarn/1.22.4/bin"
```
6. Install global dependencies (ingest-ui/client):
```
npm install -g typescript@"<3.3.0"
npm install -g node-sass@4.12.0
```
7. Install Local Packages (ingest-ui/client):
```
yarn install
```
8. Install Local Packages (ingest-ui):
```
yarn install
```
9. Set up WebStorm for starting Angular
    1. Edit Preferences:  Run/Debug configurations | Add new configuration (npm)
    2. Create for dev and local environments that run dev and local npm scripts
    3. *optional* create for other environments too (listed in package.json scripts)


#### Ingest-Client
Preferences | Project: ingest-client | Project Interpreter
[[/images/image2.png]]

### DevOps

1. Verify you can [login to aws](https://embl-ebi.awsapps.com/start#/) using your EBI credentials.
2. Setup our Infrastructure-as-Code tools following the readme in [ingest-kube-deployment](https://github.com/ebi-ait/ingest-kube-deployment)
3. If necessary, read up on [Docker](https://www.docker.com/resources/what-container) and containerisation, [get familiar with Kubernetes basics](https://github.com/HumanCellAtlas/ingest-kube-deployment), and [Helm for application management in Kubernetes](https://github.com/helm/helm).

## Some main docs
In Ingestion Service/Dev folder
* [Ingest Dev Master Document](https://docs.google.com/document/d/1sMxKPh1d_RwTwCSSX-8PzcBeQWeynwcUrXKUOyIV3xc/edit)
* [HCA Ingest Service Specification and Overall Design](https://docs.google.com/document/d/13NJdMDq6E8FDyrPebBDD4TEqmI8OXeNkp9ZquqoEhto/edit)
* [DCP System Architecture](https://docs.google.com/presentation/d/1Gm5jQJ58oXZpyBB2uadH9ce7kDcRYHLtLjLasNySKwQ/edit#slide=id.g59a933b51c_0_10)
* [HCA/ingest-client wiki](https://github.com/HumanCellAtlas/ingest-central/wiki)
* [DCP-wide Engineering Onboarding](https://github.com/HumanCellAtlas/wiki/wiki/Engineering-Onboarding) (should be one of the first docs a dev reads on joining!)

## Bookmarks
* [HCA Data Ingest - Dev](https://ui.ingest.dev.data.humancellatlas.org/)
* [The HAL Browser (for Spring Data REST) - Dev](https://api.ingest.dev.data.humancellatlas.org/browser/index.html#/)
* [HCA Metadata Schemas](https://schema.humancellatlas.org/~)
* [DCP Upload API - Swagger definition - Dev](https://upload.dev.data.humancellatlas.org/)
* [HCA Data Portal - Dev](https://dev.data.humancellatlas.org/)
* [HCA DCP DSS API - Swagger definition - Dev](https://dss.dev.data.humancellatlas.org/)
* [DCP Matrix Service API - Swagger Definition - Dev](https://matrix.dev.data.humancellatlas.org/)
* [HCA DCP Internal Tracker - Staging](https://tracker.staging.data.humancellatlas.org/)
