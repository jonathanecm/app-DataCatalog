# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import json

#Use the item sample to make sure the data structure hasn't been changed
class KaggleItem_List(scrapy.Item):
    with open('ref/kaggle_isample_list.json', 'r') as f:
        item_list = json.load(f)
        for key in item_list.keys():
            exec('{} = scrapy.Field()'.format(key))

class KaggleItem_Main(scrapy.Item):
    with open('ref/kaggle_isample_main.json', 'r') as f:
        item_main = json.load(f)
        for key in item_main.keys():
            exec('{} = scrapy.Field()'.format(key))
            
class TextItem(scrapy.Item):
    topic = scrapy.Field()
    url = scrapy.Field()
    domain = scrapy.Field()
    text = scrapy.Field()