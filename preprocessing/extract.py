import pymongo
import json
import pandas as pd

'''
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


#--Clean up
client.close()



#--Target fields
fields_main = {
    '_id': False,
    'datasetId': True,
    'title': True,
    'numberOfViews': True,
    'overview': True,
    'description': True
}
fields_list = {
    '_id': False,
    'datasetId': True,
    'categories': True
}


#--Sample query
sample_main = db['Kaggle_Main'].find({'datasetId': 13996}, fields_main)
list(sample_main)
sample_list = db['Kaggle_List'].find({'datasetId': 13996}, fields_list)    
list(sample_list)


#--Query
result_main = list(db['Kaggle_Main'].find({}, fields_main))
df_main = pd.io.json.json_normalize(result_main)
df_main.head()

result_list = list(db['Kaggle_List'].find({}, fields_list))
dict_category = {}
for doc in result_list:
    for cat in doc['categories']['categories']:
        if not dict_category.get(cat['id']):
            dict_category[cat['id']] = {
                'name': cat['name'],
                'datasetCount': cat['datasetCount'],
                'fullPath': cat['fullPath'],
                'description': cat['description']
            }
for doc in result_list:
    doc['categories'] = [cat['id'] for cat in doc['categories']['categories']]
df_list = pd.io.json.json_normalize(result_list)
df_list.head()


#--Join
df_joined = pd.merge(df_list, df_main, on='datasetId')


#--Export
df_joined.to_csv('./data/df_joined.csv', index=False)
with open('./data/dict_category.json', 'w') as f:
    json.dump(dict_category, f)
'''
#Test loading data back
pd.read_csv('/df_joined.csv', index_col=False).head()
with open('./data/dict_category.json', 'r') as f:
    print(json.load(f))


