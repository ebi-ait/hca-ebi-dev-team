---
layout: default
title:  How to force set a submission state
parent: Operations tasks
---

# How to force set a submission state 

## From Complete to Graph Valid

1. Get the token from Ingest UI in the browser via developer console network. Look for GET requests to GET/account and check the Authorization header bearer token, copy the jwt token.

1. Force set submission to be in Graph Valid state, so that it can be submitted again
   
    ``` bash
    $TOKEN=’insert-jwt-token’
    ```
1. Get the commitGraphValid link from submission hal doc resource `_links.commitGraphValid.href`
   
    ```
    curl -X PUT -H "Authorization: Bearer $TOKEN" https://api.ingest.archive.data.humancellatlas.org/submissionEnvelopes/<submission-id>/commitGraphValidEvent
    ```
1. Restart the state tracker.
    Make sure your aws creds token is updated and not expired. Get aws cli credentials from https://embl-ebi.awsapps.com/start#/

    cd to your local workspace directory for ingest-kube-deployment repo
    ```bash
    cd ingest-kube-deployment
    ```
    
    Set kubectx to point to correct env cluster
    ```bash
    kubectx ingest-eks-prod
    ```
    
    Source environment config file
    ```bash
    source config/environment_prod
    ```
    
    Restart pod
    
    ```bash
    kubectl rollout restart deployment ingest-state-tracking
    ```
    


