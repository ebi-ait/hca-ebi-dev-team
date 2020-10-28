---
layout: default
title: Retry failed ingest exporter
parent: Operations tasks
has_children: false
nav_order: 1
---

# How to retry failed bundles in the Ingest Exporter

If a submission got stuck in `Processing` state, it's possible that there are some bundles that failed to export.
Determine the cause of failure. After fixing it, the bundle exporting can be triggered again by resending the exporter messages to RabbitMQ queue

## Find the exporter messages from the logs

Currently, if a failure occurs, the exporter should log something like the following:

```
2019-08-12 15:02:59,244  - receiver.CreateBundleReceiver - ERROR in receiver.py:75 on_message(): Failed to process the exporter message: {"bundleUuid":"a0a78a4e-7891-4ef2-a22d-1bfab43ffe47","versionTimestamp":"2019-08-12T14:40:35.510354Z","messageProtocol":null,"documentId":"5d51692f1a249400085ac4d8","documentUuid":"258c06cf-f7cd-4def-8bbd-1603118897f3","callbackLink":"/processes/5d51692f1a249400085ac4d8","documentType":"Process","envelopeId":"5d51692a1a249400085ac36a","envelopeUuid":"483eb0b1-3196-4a72-9f30-4a7aecdd25b4","index":11,"total":47} due to error: An error occurred on uploading bundle files: HTTPSConnectionPool(host='upload.data.humancellatlas.org', port=443): Max retries exceeded with url: /v1/area/483eb0b1-3196-4a72-9f30-4a7aecdd25b4/supplementary_file_635648c9-dadf-43da-bb59-0fa92a1ba938.json (Caused by ResponseError('too many 500 error responses'))

```

If the submission is recent, you could get the logs using kubectl

```bash

# Confirm the count of missing bundles

$ kubectl logs -lapp=ingest-exporter | grep "2019-08-12 13"| grep  Failed | grep -c 5d5082c01a249400085abd87 # submission id

$ kubectl logs -lapp=ingest-exporter | grep "2019-08-12 13"| grep  Failed | grep -c 5d5082c01a249400085abd87 > failed-bundles-5d5082c01a249400085abd87.log
```

If the submission is not so recent, you could get the logs from Kibana using query:

Failed AND <submission-id>

Filter the log group with ingest-exporter


## Extract the messages

If there are many, save all the messages in a file as list of objects. Use this as input to the message_sender.py script in the ingest-central repo later.

```
# Using vim, extract the messages into an array of objects
$ vim failed-bundles-5d5082c01a249400085abd87.log

# In command mode, execute the following search replace commands:
# : %s/^.*{/{/g
# : %s/}.*/},/g
# Insert [ in the beginning and end of line
# To insert at the end of the line : G$ > i > ] 

```

## Resend the messages to the exporter

If there are many, Use the script in ingest-central repository:
https://github.com/HumanCellAtlas/ingest-central/blob/master/scripts/message_sender.py

Point your localhost to the RabbitMQ server:
`kubectl port-forward rabbit-0 5672:5672`

If there's only one, the RabbitMQ Management UI can be accessed to manually send the message.
`kubectl port-forward rabbit-0 15672:15672`

Go to the url : `http://localhost:15672/#`

Queue: `ingest.bundle.assay.create`
