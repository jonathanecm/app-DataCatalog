import pymongo
import json


#--Connection
with open('./scraper/ref/credential_mongo.json', 'r') as f:
    CREDENTIAL_MONGO = json.load(f)
    MONGO_URI = CREDENTIAL_MONGO['MONGO_URI']
    MONGO_DATABASE = CREDENTIAL_MONGO['MONGO_DATABASE']
    MONGO_USER = CREDENTIAL_MONGO['MONGO_USER']
    MONGO_PASSWORD = CREDENTIAL_MONGO['MONGO_PASSWORD']
connectionStr = 'mongodb://{}:{}@{}'.format(MONGO_USER, MONGO_PASSWORD, MONGO_URI)
client = pymongo.MongoClient(connectionStr)
db = client[MONGO_DATABASE]


#--Sample query
sample_main = db['Kaggle_Main'].find({'datasetId': 13996}, {
        '_id': False,
        'datasetId': True,
        'title': True,
        'numberOfViews': True,
        'overview': True,
        'description': True
    })
list(sample_main)
sample_list = db['Kaggle_List'].find({'datasetId': 13996}, {
        '_id': False,
        'datasetId': True,
        'title': True,
        'categories': True
    })    
list(sample_list)


#--Query

#Join
#Export
with open('./data/extracted.json', 'w') as f:
    json.dump(result_joined, f)


#--Clean up
client.close()