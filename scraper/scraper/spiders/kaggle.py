# -*- coding: utf-8 -*-
import scrapy
import re
import json
import logging
from scraper.items import KaggleItem_List, KaggleItem_Main


#For the meta data of the datasets on Kaggle
class KaggleSpider(scrapy.Spider):
    name = 'kaggle'
    domain = 'https://www.kaggle.com'

    #The `from_crawler` method is used as the initializer in the scraper framework (to avoid modifying the __init__ directly)
    @classmethod
    def from_crawler(cls, crawler):

        #Set up logger, create file handler and add to logger
        logger = logging.getLogger()
        fh = logging.FileHandler('./log/{}.log'.format(cls.name), mode='w')
        fh.setLevel(logging.INFO)
        logger.addHandler(fh)

        #Return the initialized obj
        return cls()

    def start_requests(self):

        #Enter from the Dataset list
        #The page setting should be moved to cli argument 
        page_start, page_end = 244, 550
        pages = range(page_start, page_end + 1)

        #Yield a request for each page
        for page in pages:
            yield scrapy.Request(url=self.domain + '/datasets?page=' + str(page), callback=self.parse_list)

    def parse_list(self, response):

        #Parse the response with xpath and re to get the list of datasets
        #The data is embedded in a chunk of js code in json format
        targetPath = '//div[@data-component-name="DatasetList"]/following-sibling::*[1]/text()'
        targetRe = r'"datasetListItems":(\[{.*\])}\)'
        data_list = response.selector.xpath(targetPath).extract_first()
        data_list = json.loads(re.search(targetRe, data_list).group(1))

        #For each dataset in the list
        for ds in data_list:

            #Yield an item for list-level meta data to the pipeline
            yield KaggleItem_List(ds)

            #Yield a request for the main page of the dataset
            request = scrapy.Request(url=self.domain + ds['datasetUrl'], callback=self.parse_main)

            #Attach the 'datasetId' for duplicate detection
            request.meta['datasetId'] = ds['datasetId']
            yield request
           
    def parse_main(self, response):

        #Parse the response with xpath and re to get the primary metadata from the main page
        #The data is embedded in a chunk of js code in json format
        targetPath = '//div[@data-component-name="DatasetContainer"]/following-sibling::*[1]/text()'
        targetRe = r'Kaggle\.State\.push\((\{.*\})\)'
        data_main = response.selector.xpath(targetPath).extract_first()
        data_main = json.loads(re.search(targetRe, data_main).group(1))

        #Yield an item for dataset-level meta data to the pipeline
        yield KaggleItem_Main(data_main)