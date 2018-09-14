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

class KagglePipeline_JsonLine(object):
    def open_spider(self, spider):
        self.exporters = {}
        self.exporters['list'] = JsonLinesItemExporter(open('../data/ds_list.json', 'ab'))
        self.exporters['main'] = JsonLinesItemExporter(open('../data/ds_main.json', 'ab'))
        for exporter in self.exporters.values():
            exporter.start_exporting()

    def close_spider(self, spider):
        for exporter in self.exporters.values():
            exporter.finish_exporting()
            exporter.file.close()

    def process_item(self, item, spider):
        if type(item) is KaggleItem_List:
            self.exporters['list'].export_item(item)
        elif type(item) is KaggleItem_Main:
            self.exporters['main'].export_item(item)
        return item

class KagglePipeline_Mongo(object):
    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item

class TextPipeline_IdDomain(object):
    domains = ['walkerland', 'pixnet']

    def process_item(self, item, spider):
        if type(item) is TextItem:
            for domain in self.domains:
                if re.search(domain, item['url']): item['domain'] = domain
        
        return item

class TextPipeline_ExtractByDomain(object):
    def unique(self, list_in): 
        #Initialize an empty list
        list_out = [] 
        
        #Traverse all elements, check if exists
        for i in list_in: 
            if i not in list_out: list_out.append(i)
                
        return list_out
    
    def extractText(self, tree, clsName, negLine):
        finder = etree.XPath('//*[@class="{}"]/descendant::p/descendant::text()'.format(clsName))
        return '\n'.join(self.unique(finder(tree))[:negLine])        
    
    def process_item(self, item, spider):
        if type(item) is TextItem:
            tree = etree.HTML(item['text'])

            if item['domain'] == 'pixnet':
                item['text'] = self.extractText(tree, 'article-content-inner', -20)
            elif item['domain'] == 'walkerland':
                item['text'] = self.extractText(tree, 'article-content-inner', -1)
    
        return item

class TextPipeline_CSV(object):
    def open_spider(self, spider):
        outputPath = Path('../data/text.csv')
        pathExist = outputPath.exists()
        self.exporter = CsvItemExporter(outputPath.open('ab'),  include_headers_line=not pathExist, lineterminator='\n')
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()

    def process_item(self, item, spider):
        if type(item) is TextItem:
            self.exporter.export_item(item)

        return item
