# -*- coding: utf-8 -*-
import scrapy
import csv

class TextSpider(scrapy.Spider):
    name = 'text'

    def start_requests(self):
        links = [
            # r'https://www.walkerland.com.tw/article/view/192591',
            r'http://drm88.pixnet.net/blog/post/35096734-肉肉山壽喜燒吃到飽%EF%BC%8C三創生活園區9f%EF%BC%8Ccp值'
        ]

        for link in links:
            request = scrapy.Request(url=link, callback=self.parse)
            request.meta['id'] = '1rr'
            yield request
           
    def parse(self, response):
        targetPath = '//p/parent::*'
        paragraphs = response.selector.xpath(targetPath).extract()
        text = '\n'.join(paragraphs)

        # yield TextItem()
        # with open('some.csv', 'a', newline='', encoding='utf-8') as f:
        #     writer = csv.writer(f)
        #     writer.writerow([response.meta['id'], text])