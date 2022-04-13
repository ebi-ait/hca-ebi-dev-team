---
layout: default
title: Create wrangler user in the wrangling EC2 instance
parent: Operations tasks
---

# Create  Create wrangler user in the wrangling EC2 instance
Wranglers need access to the `hca-wrangler-tools-ec2` and a developer must give them this. The below steps assume that you have the correct account privileges in AWS.

1. login to [AWS console](https://embl-ebi.awsapps.com/start#/)
2. Copy the value of `ingest/tool/wrangler/ec2` in [AWS secrets manager](https://console.aws.amazon.com/secretsmanager/home?region=us-east-1#!/secret?name=ingest%2Ftool%2Fwrangler%2Fec2).
3. Paste that value into a new SSH key in your machine (e.g. `~/.ssh/WranglerAdmin.pem`). Make sure the contents of this file are correctly formatted.
4. Ask the wrangler for their desired username
5. Ask the wrangler for their **public** SSH key
    - `ssh-keygen -t rsa -b 4096 -C "WRANGLER_USERNAME"` to generate public/private key pair
    - Note: **private** keys should never be transmitted over insecure protocols.
6. SSH into the ec2 instance using `ssh -i "PATH_TO_FILE_IN_STEP_2" ubuntu@tool.archive.data.humancellatlas.org`
7. Run `sudo ./create_wrangler.sh` and follow the steps
8. Check and add the user created to group docker
    - `getent group`
    -  `usermod -a -G docker "WRANGLER_USERNAME"`
9. Instruct the wrangler to try `ssh WRANGLER_USERNAME@tool.archive.data.humancellatlas.org`. In case the wrangler has multiple ssh keys on their system, they could try `ssh -i "PATH_TO_PRIVATE_KEY_GENERATED_IN_STEP_4" WRANGLER_USERNAME@tool.archive.data.humancellatlas.org` 
