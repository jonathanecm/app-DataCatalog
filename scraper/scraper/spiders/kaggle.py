# -*- coding: utf-8 -*-
import scrapy
import re
import json


class KaggleSpider(scrapy.Spider):
    name = 'kaggle'

    def start_requests(self):
        #Enter from the Dataset list
        url_base = 'https://www.kaggle.com/datasets?page='
        headers = {
            'Accept': '*/*',
            'User-Agent': self.settings['USERAGENT_CANDIDATES'][0]
        }

        page_start, page_end = 1, 1
        pages = range(page_start, page_end + 1)

        for page in pages:
            url = url_base + str(page)
            yield scrapy.Request(url=url, headers=headers, callback=self.parse_list)

    def parse_list(self, response):
        targetPath = '//div[@data-component-name="DatasetList"]/following-sibling::*[1]/text()'
        targetRe = r'"datasetListItems":(\[{.*\])}\)'
        data_dataset = response.selector.xpath(targetPath).extract()[0]
        data_dataset = json.loads(re.findall(targetRe, data_dataset)[0])
        
        with open('dataOutput.json', 'w') as f:
            json.dump(data_dataset, f)

    def parse_main(self, response):
        pass

    def parse_overview(self, response):
        pass

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
