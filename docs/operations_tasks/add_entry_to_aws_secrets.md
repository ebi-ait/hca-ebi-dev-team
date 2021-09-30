---
layout: default
title: Add an entry to our secrets stored on AWS
parent: Operations tasks
---

# Add an entry to our secrets that is stored on AWS
The below steps assume that you have the correct account privileges in AWS.

1. Log in to your HCA's AWS account
2. Make sure that you are at the right AWS region otherwise you won't able to see/manage our secrets stored in the Secret Manager.
   The region should be set to: `us-east-1` (N. Virginia)
3. Go to Secrets Manager. You can do it with any of the follong way:
   - click `Secters Manager` on the recently visited links section if its is not your first time,
   - select the Services drop-down and in the Security, Identity, & Compliance section click on `Secrets Manager` link,
   - Type `Secters Manager` into the search bar and click on the appearing `Secrets Manager` link
4. Click on the Secrets option on the left hand side menu bar
5. Depending on which environment you would like to add the new secret you should type `ingest/{ENV_NAME}/secrets` to the search bar
   where `ENV_NAME` is a placeholder and can be the following values: `dev`, `staging` and `prod`.
6. Click on the name of the secret, for example `ingest/dev/secrets`.
7. Scroll down to the `Secret value` section and click on the `Retrieve secret value` button.
8. Click omn the `Edit` button and add your secrets as key/value pairs.
9. When you finished adding all your new secrets click on the `Save` button to store it.

## Add a secret to the deployment as environment variable
10. Modify the `deployment.yaml` file under `apps/<APPLICATION_NAME>/templates` folder,
   where `APPLICATION_NAME` reflects the name of the application the secrets will be used
11. Adds your secret under the environment variables (`spec.template.spec.containers.env`).
   Define the name and value of your environment variable.
   If the value comes from AWS secret manager then use this format:
   ```yaml
   - name: ENV_VARIABLE_NAME
     valueFrom:
       secretKeyRef:
         key: SERVICE-PASSWORD
         name: api-keys
   ```

## Add secret to the deployment configuration
12. Modify the `deploy_secrets` shell script under the `scripts` folder and add your secret value below the `get_secret`
    method call and after the `helm upgrade secrets secrets\` line as you can see it the script.
   
## Define your secret in the deployment template
13. Modify the `deployment.yaml` file under `secrets/templates` folder and add your secret definition under the `data` key.

## Deploy the new secret value
14. Go to the `apps` folder
15. Execute the following command in the command line:

`make deploy-secrets`
