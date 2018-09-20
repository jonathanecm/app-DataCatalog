# -*- coding: utf-8 -*-
import scrapy
import csv
import logging
from scraper.items import TextItem


#For general usage of extracting plain text data
class TextSpider(scrapy.Spider):
    name = 'text'
    
    @classmethod
    def from_crawler(cls, crawler):
        
        #Setup logger, create file handler and add to logger
        logger = logging.getLogger()
        fh = logging.FileHandler('./log/{}.log'.format(cls.name), mode='w')
        fh.setLevel(logging.INFO)
        logger.addHandler(fh)

        return cls()

    def start_requests(self):
        
        #Start with a list of target urls and corresponding topics from a csv file
        with open('./ref/text_url.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)

            #Skip the first row (the column names)
            colName = reader.__next__()

            #Parse each row and yield requests
            for row in reader:
                request = scrapy.Request(url=row[4], callback=self.parse)
                request.meta['topic'] = row[1]
                yield request
    
    def parse(self, response):

        #Find all p elements and their parents
        targetPath = '//p/parent::*'
        textElements = response.selector.xpath(targetPath).extract()

        #Join all found elements into a single string for pipeline processing
        textElements = '\n'.join(textElements)

        yield TextItem(topic=response.meta['topic'], url=response.url, text=textElements)