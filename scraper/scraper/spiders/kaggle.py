# -*- coding: utf-8 -*-
import scrapy
import re
import json


class KaggleSpider(scrapy.Spider):

    name = 'kaggle'
    domain = 'https://www.kaggle.com'

    #Generate random header for each request
    def generateHeaders(self, id=0):
        headers = {
            'Accept': '*/*',
            'User-Agent': self.settings['USERAGENT_CANDIDATES'][id]
        }
        return headers

    def start_requests(self):
        #Enter from the Dataset list
        page_start, page_end = 1, 1
        pages = range(page_start, page_end + 1)
        headers = self.generateHeaders()

        for page in pages:
            yield scrapy.Request(url=self.domain + '/datasets?page=' + str(page), headers=headers, callback=self.parse_list)

    def parse_list(self, response):
        targetPath = '//div[@data-component-name="DatasetList"]/following-sibling::*[1]/text()'
        targetRe = r'"datasetListItems":(\[{.*\])}\)'
        data_list = response.selector.xpath(targetPath).extract_first()
        data_list = json.loads(re.search(targetRe, data_list).group(1))
        
        with open('ds_list.json', 'a') as f:
            json.dump(data_list, f)

        for ds in data_list:
            headers = self.generateHeaders()
            yield scrapy.Request(url= self.domain + ds['datasetUrl'], headers=headers, callback=self.parse_main)
            break
           
    def parse_main(self, response):
        targetPath = '//div[@data-component-name="DatasetContainer"]/following-sibling::*[1]/text()'
        targetRe = r'Kaggle\.State\.push\((\{.*\})\)'
        data_main = response.selector.xpath(targetPath).extract_first()
        data_main = json.loads(re.search(targetRe, data_main).group(1))

        with open('ds_main.json', 'a') as f:
            json.dump(data_main, f)