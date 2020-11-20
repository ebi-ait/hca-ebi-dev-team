---
layout: default
title: Git secrets setup
parent: Admin and Setup
---

# Git Secrets Setup

Git secrets - Prevents you from committing secrets and credentials into git repositories.

This guides was initially for the HCA team at the EBI but applies across the AIT group.

## 1. Install 

```
git clone https://github.com/awslabs/git-secrets.git
(cd git-secrets && sudo make install)
```

or using homebrew for mac: `brew install git-secrets`
 
## 2. Configure

Adds common AWS patterns to the git config and ensures that keys present
    in ``~/.aws/credentials`` are not found in any commit.

`git secrets --register-aws --global`


From documentation, `--register-aws` adds the following check:

    - AWS Access Key IDs via ``(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}``
    - AWS Secret Access Key assignments via ":" or "=" surrounded by optional
      quotes
    - AWS account ID assignments via ":" or "=" surrounded by optional quotes
    - Allowed patterns for example AWS keys (``AKIAIOSFODNN7EXAMPLE`` and
      ``wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY``)
    - Known credentials from ``~/.aws/credentials``

    .. note::

        While the patterns registered by this command should catch most
        instances of AWS credentials, these patterns are **not** guaranteed to
        catch them **all**. ``git-secrets`` should be used as an extra means of
        insurance -- you still need to do your due diligence to ensure that you
        do not commit credentials to a repository.

Adding `--global` flag will apply the configuration globally (spans across all repos)

Add secret patterns:

`git secrets --add --literal '<literal>'`

Add secret pattern globally:

```
git secrets --add --literal '<literal>' --global

```

If you use other cloud providers you should also add secret patterns specific for them. For example, the HCA teams uses GCP accounts for DCP authentication so you need to add the following:
```
git secrets --add --literal 'private_key' --global
git secrets --add --literal 'client_id' --global
git secrets --add --literal 'client_email' --global
git secrets --add --literal 'private_key_id' --global

```

**If you're in AIT and use another cloud infrastructure please add the details here.**
 
## 3. Verify that whitelisted or prohibited items are configured:

For current repo:
`git secrets --list`
 
For all repo:
`git secrets --list --global`

```
secrets.providers git secrets --aws-provider
secrets.patterns (A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}
secrets.patterns ("|')?(AWS|aws|Aws)?_?(SECRET|secret|Secret)?_?(ACCESS|access|Access)?_?(KEY|key|Key)("|')?\s*(:|=>|=)\s*("|')?[A-Za-z0-9/\+=]{40}("|')?
secrets.patterns ("|')?(AWS|aws|Aws)?_?(ACCOUNT|account|Account)_?(ID|id|Id)?("|')?\s*(:|=>|=)\s*("|')?[0-9]{4}\-?[0-9]{4}\-?[0-9]{4}("|')?
secrets.patterns private_key
secrets.patterns client_id
secrets.patterns client_email
secrets.patterns private_key_id
secrets.allowed AKIAIOSFODNN7EXAMPLE
secrets.allowed wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

```

## 4. Configure so that the hooks will be installed whenever you create or clone new git repositories:

```
git secrets --install ~/.git-templates/git-secrets
git config --global init.templateDir ~/.git-templates/git-secrets
```

## 5. Install hooks

To install hooks for specific repos that existed before global configuration was set up:
```
cd /path/to/my/repo
git secrets --install
``` 

You need to add hooks to all your local repositories

If you have an exclusive directory which contains all your github repo in one level (i.e. no sudirectories which contains github repos), you can use the following command: 
```
find . -maxdepth 1 -mindepth 1 -type d -exec sh -c '(echo {} && cd {} && git secrets --install && echo)' \;
``` 

## 6. Verify that secrets are not being committed

To test if git secrets works for GCP accounts, try the ff steps:

* Create a fake GCP account json file in any github repository:
```
  {
 "type": "service_account",
 "project_id": "your-project-id",
 "private_key_id": "randomsetofalphanumericcharacters",
 "private_key": "-----BEGIN PRIVATE KEY-----\thisiswhereyourprivatekeyis\n-----END PRIVATE KEY-----\n",
 "client_email": "keyname@your-project-id.iam.gserviceaccount.com",
 "client_id": "numberhere",
 "auth_uri": "https://accounts.google.com/o/oauth2/auth",
 "token_uri": "https://accounts.google.com/o/oauth2/token",
 "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
 "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/keyname%40your-project-id.iam.gserviceaccount.com"
}
```
* Add and commit

```
git add <fake-gcp-file.json>
git commit -m 'Testing committing gcp file'
```


* The following error should be displayed:
```fake.json:4: "private_key_id": "randomsetofalphanumericcharacters",
fake.json:5: "private_key": "-----BEGIN PRIVATE KEY-----\thisiswhereyourprivatekeyis\n-----END PRIVATE KEY-----\n",
fake.json:6: "client_email": "keyname@your-project-id.iam.gserviceaccount.com",
fake.json:7: "client_id": "numberhere",

[ERROR] Matched one or more prohibited patterns

Possible mitigations:
- Mark false positives as allowed using: git config --add secrets.allowed ...
- Mark false positives as allowed by adding regular expressions to .gitallowed at repository's root directory
- List your configured patterns: git config --get-all secrets.patterns
- List your configured allowed patterns: git config --get-all secrets.allowed
- List your configured allowed patterns in .gitallowed at repository's root directory
- Use --no-verify if this is a one-time false positive
```
 
# References
  * GitHub - https://github.com/awslabs/git-secrets
  * Guidelines from Greenbox - https://docs.google.com/document/d/1_7deaZd2XbjUetVJs8EsQg6JbW_MEX2iFgXpnR_PyYs/edit#
  * GCP Accounts - https://cloud.google.com/blog/products/gcp/help-keep-your-google-cloud-service-account-keys-safe
  * Simpler steps in DCP wiki: https://allspark.dev.data.humancellatlas.org/dcp-ops/docs/wikis/Git%20Secrets
# See Also
  * Gitlab Preventing pushes of secrets - https://docs.gitlab.com/ee/push_rules/push_rules.html#prevent-pushing-secrets-to-the-repository