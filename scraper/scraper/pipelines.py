# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scraper.items import *
from scrapy.exporters import JsonLinesItemExporter, CsvItemExporter
from lxml import etree
from pathlib import Path
import pymongo
import re
import uuid


'''
------------------------------------------------------------
Kaggle Middlewares
------------------------------------------------------------
'''
#--Save Kaggle items in a jsonline file
class KagglePipeline_JsonLine(object):

    #Create exporters for both types of items
    def open_spider(self, spider):
        self.exporters = {}
        self.exporters['list'] = JsonLinesItemExporter(open('../data/ds_list.json', 'ab'))
        self.exporters['main'] = JsonLinesItemExporter(open('../data/ds_main.json', 'ab'))
        for exporter in self.exporters.values():
            exporter.start_exporting()

    #Close the exporters
    def close_spider(self, spider):
        for exporter in self.exporters.values():
            exporter.finish_exporting()
            exporter.file.close()

    #Save the items respectively
    def process_item(self, item, spider):
        if type(item) is KaggleItem_List:
            self.exporters['list'].export_item(item)
        elif type(item) is KaggleItem_Main:
            self.exporters['main'].export_item(item)
        return item


#--Save Kaggle items in a Mongo db
class KagglePipeline_Mongo(object):

    #Collection names in the db
    COLLECTION_LIST = 'Kaggle_List'
    COLLECTION_MAIN = 'Kaggle_Main'

    #Acquire Mongo credential from setting
    @classmethod
    def from_crawler(cls, crawler):
        cls.mongo_uri=crawler.settings.get('MONGO_URI'),
        cls.mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        return cls()

    #Establish db connection
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    #Close db connection
    def close_spider(self, spider):
        self.client.close()

    #Examine if the entry has already existed and save/replace the item accordingly
    def process_item(self, item, spider):
        if type(item) is KaggleItem_List:
            exist = self.db[self.COLLECTION_LIST].find_one_and_replace({'datasetId': item['datasetId']}, dict(item))
            if not exist: self.db[self.COLLECTION_LIST].insert_one(dict(item))
        elif type(item) is KaggleItem_Main:
            exist = self.db[self.COLLECTION_MAIN].find_one_and_replace({'datasetId': item['datasetId']}, dict(item))
            if not exist: self.db[self.COLLECTION_MAIN].insert_one(dict(item))
        return item




'''
------------------------------------------------------------
Pure Text Middlewares
------------------------------------------------------------
'''
#--Identify and record the domain of the url
class TextPipeline_IdDomain(object):

    #Domain candidates
    domains = ['walkerland', 'pixnet']

    def process_item(self, item, spider):
        if type(item) is TextItem:
            item['domain'] = 'other'
            for domain in self.domains:
                if re.search(domain, item['url']): item['domain'] = domain

        return item


#--Extract the text by domain
class TextPipeline_ExtractByDomain(object):

    #Remove the duplicate item in a list
    def unique(self, list_in): 
        #Initialize an empty list
        list_out = [] 
        
        #Traverse all elements, check if exists
        for i in list_in: 
            if i not in list_out: list_out.append(i)
                
        return list_out
    
    #Extract the text by filtering the class of the parent of each p
    def extractText(self, tree, eFilter, negLine):
        finder = etree.XPath('//*{}/descendant::p/descendant::text()'.format(eFilter))
        return '\n'.join(self.unique(finder(tree))[:negLine])        
    
    #Process text according to the domain, applying different filter
    def process_item(self, item, spider):
        if type(item) is TextItem:
            tree = etree.HTML(item['text'])

            #Skip the last couple of lines to remove the irrelevant content, often some ads or links to other articles
            if item['domain'] == 'pixnet':
                item['text'] = self.extractText(tree, '[@class="article-content-inner"]', -20)
            elif item['domain'] == 'walkerland':
                item['text'] = self.extractText(tree, '[@class="article-content-inner"]', -5)
            else: item['text'] = self.extractText(tree, '', -5)
    
        return item


#--Save the text in a csv file
class TextPipeline_CSV(object):

    #Create the csv exporter
    def open_spider(self, spider):
        outputPath = Path('../data/text_{}.csv'.format(str(uuid.uuid4())))
        pathExist = outputPath.exists()
        self.exporter = CsvItemExporter(outputPath.open('wb'),  include_headers_line=not pathExist, lineterminator='\n')
        self.exporter.start_exporting()

    #Close the exporter
    def close_spider(self, spider):
        self.exporter.finish_exporting()

    #Export each item
    def process_item(self, item, spider):
        if type(item) is TextItem:
            self.exporter.export_item(item)

        return item
