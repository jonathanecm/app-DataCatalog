# -*- coding: utf-8 -*-
import scrapy
import csv
import logging
from scraper.items import TextItem

class TextSpider(scrapy.Spider):
    name = 'text'
    logging.basicConfig(
        filename='log/text.log',
        filemode='w'
    )

    def start_requests(self):
        #Csv with column name, with topic in the first column and target url in the second
        with open('./ref/text_urls.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            colName = reader.__next__()
            for row in reader:
                request = scrapy.Request(url=row[1], callback=self.parse)
                request.meta['topic'] = row[0]
                yield request
           
    def parse(self, response):
        targetPath = '//p/parent::*'
        textElements = response.selector.xpath(targetPath).extract()
        textElements = '\n'.join(textElements)

        yield TextItem(topic=response.meta['topic'], url=response.url, text=textElements)