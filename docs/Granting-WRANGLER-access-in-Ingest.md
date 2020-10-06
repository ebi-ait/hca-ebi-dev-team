# Granting WRANGLER access to Ingest UI

To give a registered user (via Ingest UI) a WRANGLER access in Ingest:

1. SSH into mongo pod 
```
$ kubectx ingest-eks-prod
$ source config/environment_prod
$ kubectl exec -it mongo-0 -- sh
```
2. Start mongo shell
```
$ mongo
```
3. Point to admin db
```
$ use admin
```
4. Find account by name
Query all and inspect result
```
> db.account.find()
```
OR filter the result by name
```
> db.account.find({name: {$regex: "Ray"}})
```
5. Copy account object id and use it in the update query
```
> db.account.update({ "_id" : { $in:[ObjectId("5ece3464ec0680746267e784")]}}, {$set: {"roles": ["CONTRIBUTOR", "WRANGLER"]}} )
```
