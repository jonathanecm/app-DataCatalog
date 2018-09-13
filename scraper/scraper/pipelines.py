# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonLinesItemExporter
import pymongo

class KagglePipeline(object):
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
        if 'downloadCount' in item.keys():
            self.exporters['list'].export_item(item)
        if 'description' in item.keys():
            self.exporters['main'].export_item(item)
        return item

class MongoPipeline(object):
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
