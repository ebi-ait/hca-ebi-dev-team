---
layout: default
title: Track Duplicate Bundles
parent: Misc
---

# Track Duplicate Bundles

This guide is based on the procedures used to [track the missing bundles for the Tabula Muris (TM) dataset in production](https://github.com/HumanCellAtlas/ingest-central/issues/343). Other datasets might have slightly different structures, some of the points here might not apply. However, the hope is that the general guidelines remain useful.

## Overview

* Verifying discrepancies between bundle manifest and error logs
* Retrieving candidate assaying processes
* Determining assaying processes from duplicated bundles

## Verifying Discrepancies

For TM dataset, there are a total of 99,840 bundles expected but only 99,495 were successfully exported to the Data Store. The logs indicate a total of 349 failed exports, which did not add up exactly with was reported in the bundle manifests. To see if any of those reported failures were somehow false negatives, the reported processes needed to be cross checked with the bundle manifest. Since the bundle manifests only contain the process UUIDs, a list of UUIDs were retrieved by using the list of process id's extracted from the logs.

```
for process_id in $(cat process_ids.lst); do \
curl -s https://api.ingest.data.humancellatlas.org/processes/${process_id} | \
jq '.uuid.uuid' | sed 's/"//g"' > process_uuids.lst
```

---
**Legacy UUID Subtype**

Alternatively, the UUIDs could have been retrieved directly from the MongoDB database, and this was actually the original approach. However, at the time, UUIDs stored in the database use the legacy 0x03 `BinData` format that made it difficult--almost impossible--to retrieve the UUIDs in proper format. Bundle manifests are created using a different encoding for the UUIDs, and they don't directly link back to the metadata; they only record the string representations of the UUIDs.

---

With a list of process UUIDs, the manifests can be checked for any bundles that contain any of the processes that were reported to have failed. *Note that this only works under the assumption that bundles can only contain exactly one assaying process*. With MongoDB running the Kubernetes cluster as `mongo-0`, the check can be done like:

```
for process_uuid in $(cat process_uuids.lst); do \
kubectl exec -it mongo-0 -- bash -c "mongo admin --quiet --eval \
'db.bundleManifest.findOne({\
  envelopeUuid: \"${REPLACE_WITH_ENVELOPE_UUID}\", \
  \"fileProcessMap.${process_uuid}\": {\$exists: true}\
})'"; done | grep -vE '^null.*$'
```

---

**Evaluating MongoDB Query with Local Shell Variables**

Notice in the query above that instead of directly invoking `mongo` on the `mongo-0` pod, it is passed as command line argument to `bash`. This is made to be able to supply local shell variables to the MongoDB query.

---


If the command above returns a non-null database object, it means one of processes matched a bundle manifest, which means it's been exported successfully. However, in the case of TM, there was none, and so the conclusion was that all processes that were reported to have failed exporting actually failed. The only other possibility is for 4 out of the 99,495 bundles that were successfully exported to be duplicates.

## Retrieving Candidate Assaying Processes

At the time of writing, bundle UUIDs are dynamically generated that even duplicate ones don't share the same UUIDs. There is also no straightforward approach to determine which of the processes in a bundle is the assaying process. The only way to check if any 2 or more bundles are duplicates of each other is to check if they have the same list of processes (one of which will be the assaying one). This can be done with a set of common shell scripting tools by formatting MongoDB query results in such a way that supports string manipulation. Once all the bundle manifests are represented as a concatenation of all the process UUIDs, it should be easy to see which ones appear more than once.

```
kubectl exec -it mongo-0 -- mongo admin --quiet --eval \
'db.bundleManifest.find({envelopeUuid: "REPLACE_WITH_ENVELOPE_UUID"})\
.forEach(function(manifest) { \
  var keys = []; for (var key in manifest.fileProcessMap) keys.push(key); \
  keys.sort(); print(keys)})' | \
  sort | uniq -c | grep -vE '^[[:blank:]]*1 ' | \
  awk -v RS='\r\n' '{split($2, result, ","); \
  for (i in result) print result[i]}' > candidate_process_uuids.lst
```

In the command above, `-v RS='\r\n'` ensures that `awk` uses the same record separator (RS) sequence regardless of which platform it runs. Without this, the record separator may end up being something unexpected ([like the `^M` character](https://stackoverflow.com/a/13082137/404604)).

`candidate_process_uuids.lst` should contain a list of process UUIDs for processes that could be the assaying process for which a bundle was duplicated.


## Determining Assaying Processes from Duplicated Bundles

For this procedure to work, a few assumptions are made. First, as previously mentioned, bundles contain exactly one assaying process. Another is that assaying process id's are tracked manually (i.e. process id's are specified in the spreadsheet). It is specially helpful if the manually assigned process ids are easily distinguishable from dynamically generated ones. For example, in the case of the TM dataset, manually assigned process id's start with `Process_` while the generated ones start with `process_id_`. With this in place, the final thing to do is get all candidate processes by their UUIDs and filter them based on the `process_id` field:

```
for uuid in $(cat duplicate_candidates.lst); do \
curl -s https://api.ingest.data.humancellatlas.org/processes/search/findByUuid?uuid=$uuid | \
jq '[.content.process_core.process_id, ._links.self.href, .uuid.uuid] | \
"\(.[0]) \(.[1]) \(.[2])"'; done | grep -oE 'Process.*' |  sed 's/"//g' \
> duplicate_bundle_processes.lst
```

As mentioned above, this filtering works because assaying processes for the TM dataset were assigned easily distinguishable id's (`Process.*`). This results in a list of space separated data pertaining to the assaying processes whose exporting resulted in duplicate bundles. Each row displays the process id, API url for the process resource, and the uuid. To display only the relevant, UUIDs from the results, the 3rd column can be printed with `awk '{print $3}'`.

Once the list of process UUIDs is compiled, the final thing to do is to map them back to the duplicate bundles in order to determine which ones are duplicates of each other. The following command formats results similar to how YAML represents a mapping of lists, but it can be modified to display results differently:

```
for uuid in $(cat duplicate_bundle_processes.lst | awk '{print $3}'); do \
echo "${uuid}:"; \
kubectl exec -it mongo-0 -- mongo admin --quiet --eval \
'db.bundleManifest.find({envelopeUuid:"REPLACE_WITH_ENVELOPE_UUID"})\
.forEach(function(manifest) { \
  var keys = []; \
  for (var key in manifest.fileProcessMap) keys.push(key); \
  keys.sort(); \
  print(manifest.bundleUuid + " " +keys)})' | \
grep $uuid | \
awk '{printf "  - %s\n", $1}'; done
```
