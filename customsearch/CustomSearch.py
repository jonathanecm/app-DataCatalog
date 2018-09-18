from apiclient.discovery import build
from collections import namedtuple
from pprint import pprint
import pandas as pd
import re
import json
import argparse


#--Google Cloud API reference
#https://developers.google.com/api-client-library/python/start/get_started
#https://developers.google.com/api-client-library/python/apis/customsearch/v1
#http://google.github.io/google-api-python-client/docs/epy/googleapiclient.discovery-module.html#build


#--Parse CLI args
#Provide mode to examine single search response item
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--item", help="print response item structure", action="store_true")
args = parser.parse_args()


#--Parse config and credential from files
with open('config.json', 'r', encoding='utf-8') as f:
    dic = json.load(f)
    CONFIG = namedtuple("Config", dic.keys())(*dic.values())

with open(CONFIG.CREDENTIAL_FILE, 'r') as f:
    dic = json.load(f)
    CREDENTIAL = namedtuple("Credential", dic.keys())(*dic.values())


#--Initialize api service and output df, read in topics (search terms) from file
service = build(serviceName='customsearch', version='v1', developerKey=CREDENTIAL.API_KEY)
topics = pd.read_csv(CONFIG.TOPIC_FILE, header=None)[0]
df_results = pd.DataFrame(columns=['topic', 'domain', *CONFIG.TARGET_FIELDS])


#--Operate search
#`start` is the start index of the search result
#i.e. start=11 fetches the second page result 
for topic in topics:
    response = service.cse().list(
        q=topic + ' ' + CONFIG.MODIFIER,
        cx=CREDENTIAL.CUSTOM_ENGINE_ID,
        start=1
    ).execute()

    if args.item:
        pprint(response['items'][0])
        break

    #For each item in response, check the domain in `displayLink`
    #Create 'item_out' with format matching columns in the `df_results`
    for item in response['items']:
        for domain in CONFIG.DOMAINS:
            if re.search(domain, item['displayLink']):
                item_out = {}
                item_out['topic'] = topic
                item_out['domain'] = domain
                for targetField in CONFIG.TARGET_FIELDS:
                    item_out[targetField] = item[targetField]
                df_results = df_results.append(item_out, ignore_index=True)


#--If not in 'item' mode, export df into csv
if not args.item:
    df_results.to_csv(CONFIG.RESULT_FILE, encoding='utf-8')