# -*- coding: utf-8 -*-
import scrapy
import csv

class TextSpider(scrapy.Spider):
    name = 'text'

    def start_requests(self):
        links = [
            r'http://may1215may.pixnet.net/blog/post/403068155-「肉肉山」壽喜燒%2C吃到飽%2C三創生活園區9樓%2C'
        ]

        for link in links:
            request = scrapy.Request(url=link, callback=self.parse_main)
            request.meta['id'] = '1rr'
            yield request
           
    def parse_main(self, response):
        targetPath = '//p/*/text()'
        paragraphs = response.selector.xpath(targetPath).extract()
        text = '\n'.join(paragraphs)

        with open('some.txt', 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)

        # with open('some.csv', 'a', newline='', encoding='utf-8') as f:
        #     writer = csv.writer(f)
        #     writer.writerow([response.meta['id'], text])
        