# Fixes https://github.com/ebi-ait/hca-ebi-dev-team/issues/382
from bson import ObjectId, DBRef
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['admin']

invalid_count = 0
total_count = 0
valid_count = 0
corrected_count = 0

collections = ['biomaterial', 'process', 'protocol', 'file']

for collection in collections:
    print(f'===== {collection} =====')
    for doc in db[collection].find():
        project = doc.get('project')
        if project and isinstance(project.id, str):
            invalid_count = invalid_count + 1
            id = ObjectId(doc.get('_id'))
            db[collection].update_one(
                {
                    '_id': id
                },
                {
                    "$set": {
                        'project': DBRef('project', ObjectId(project.id))
                    }
                }
            )
            corrected_count = corrected_count + 1
            print(f'corrected {collection}: {corrected_count}', end='\r')
        else:
            valid_count = valid_count + 1
        total_count = total_count + 1

    print(f'invalid: {invalid_count}')
    print(f'corrected: {corrected_count}')
    print(f'valid: {valid_count}')
    print(f'total: {total_count}')
