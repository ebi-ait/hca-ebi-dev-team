---
layout: default
title: User Account Cleanup
parent: Operations tasks
---

Every 3 months inactive accounts should be disabled. After 3 more omnths, if there is no complaint, they can be safely deleted.

## Disable accounts not active in 2006
```bash
aws iam get-credential-report --output text --query 'Content' | base64 --decode | cut -d',' -f1,11 | sort -t, -k2 | grep -v '2026' | cut -d, -f1 | grep -v '<' | grep -v 'sa-' | xargs -I{} sh -c 'aws iam list-access-keys --query 'AccessKeyMetadata[].AccessKeyId' --output text --user-name {} | xargs -n1 | xargs -i[] -t aws iam update-access-key --user-name {} --access-key-id [] --status Inactive'
```

## Remove Wrangler Access from MongoDB
```javascript
use('admin');
db.getCollection('account').updateMany(
    { name: { '$regex': 'Amnon Khen' } },
    { $pull: { roles: "WRANGLER" } }
);
```
