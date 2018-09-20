import pymongo
import json
with open('./scraper/ref/credential_mongo.json', 'r') as f:
    CREDENTIAL_MONGO = json.load(f)
    MONGO_URI = CREDENTIAL_MONGO['MONGO_URI']
    MONGO_DATABASE = CREDENTIAL_MONGO['MONGO_DATABASE']

client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DATABASE]
db.list_collection_names()
#Collection is automatically created when used 

result = db['Kaggle_Main'].find({}, {
        '_id': False,
        'datasetId': True
    })
ids = [item['datasetId'] for item in list(result)]
398 in ids

result = db['Kaggle_List'].find({
        'datasetId': 13996
    }, {
        '_id': False,
        'title': True
    })
list(result)

db['Kaggle_List'].find_one_and_delete({
    'datasetId': 3759
})

client.close()