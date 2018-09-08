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
        data_dataset = response.selector.xpath(targetPath).extract()[0]
        data_dataset = json.loads(re.findall(targetRe, data_dataset)[0])
        headers = self.generateHeaders()
        
        with open('dataOutput.json', 'w') as f:
            json.dump(data_dataset, f)

        for ds in data_dataset:
            yield scrapy.Request(url= self.domain + ds['datasetUrl'] + '/home', headers=headers, callback=self.parse_overview)
            break
           
    def parse_main(self, response):
        pass

    def parse_overview(self, response):
        targetPath = '//div[@data-component-name="DatasetContainer"]/following-sibling::*[1]/text()'
        targetRe = r'Kaggle\.State\.push\((\{.*\})\)'
        overview = response.selector.xpath(targetPath).extract()[0]
        overview = json.loads(re.findall(targetRe, overview)[0])['description']
        self.logger.info(overview)

    def parse(self, response):
        #Save the html
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.logger.info('Saved file %s' % filename)

        #Save the parsed items
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }
        
        #Following request
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)           
