# -*- coding: utf-8 -*-
import scrapy
import re
import json
import logging
from scraper.items import KaggleItem_List, KaggleItem_Main

class KaggleSpider(scrapy.Spider):
    name = 'kaggle'
    domain = 'https://www.kaggle.com'

    #The `from_crawler` method is used as the initializer in the scraper framework (to avoid modifying the __init__ directly)
    @classmethod
    def from_crawler(cls, crawler):
        #Create file handler and add to logger
        logger = logging.getLogger()
        fh = logging.FileHandler('./log/{}.log'.format(cls.name), mode='w')
        fh.setLevel(logging.INFO)
        logger.addHandler(fh)

        #Return the initialized obj
        return cls()

    def start_requests(self):
        #Enter from the Dataset list
        #The page setting should be moved to cli argument 
        page_start, page_end = 1, 550
        pages = range(page_start, page_end + 1)

        #Yield a request for each page
        for page in pages:
            yield scrapy.Request(url=self.domain + '/datasets?page=' + str(page), callback=self.parse_list)

    def parse_list(self, response):
        #Parse the response with xpath and re to get the list of datasets
        targetPath = '//div[@data-component-name="DatasetList"]/following-sibling::*[1]/text()'
        targetRe = r'"datasetListItems":(\[{.*\])}\)'
        data_list = response.selector.xpath(targetPath).extract_first()
        data_list = json.loads(re.search(targetRe, data_list).group(1))

        for ds in data_list:
            yield KaggleItem_List(ds)

            request = scrapy.Request(url=self.domain + ds['datasetUrl'], callback=self.parse_main)
            request.meta['datasetId'] = ds['datasetId']
            yield request
           
    def parse_main(self, response):
        targetPath = '//div[@data-component-name="DatasetContainer"]/following-sibling::*[1]/text()'
        targetRe = r'Kaggle\.State\.push\((\{.*\})\)'
        data_main = response.selector.xpath(targetPath).extract_first()
        data_main = json.loads(re.search(targetRe, data_main).group(1))

        yield KaggleItem_Main(data_main)