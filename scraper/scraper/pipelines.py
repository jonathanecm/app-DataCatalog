# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonLinesItemExporter

class KagglePipeline(object):
    def open_spider(self, spider):
        self.exporters = {}
        self.exporters['list'] = JsonLinesItemExporter(open('ds_list.jsl', 'ab'))
        self.exporters['main'] = JsonLinesItemExporter(open('ds_main.jsl', 'ab'))
        for exporter in self.exporters.values():
            exporter.start_exporting()

    def close_spider(self, spider):
        for exporter in self.exporters.values():
            exporter.finish_exporting()
            exporter.file.close()

    def process_item(self, item, spider):
        if 'downloadCount' in item.keys():
            self.exporters['list'].export_item(item)
        if 'description'in item.keys():
            self.exporters['main'].export_item(item)
        return item
