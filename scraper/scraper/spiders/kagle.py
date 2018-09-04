# -*- coding: utf-8 -*-
import scrapy


class KagleSpider(scrapy.Spider):
    name = 'kagle'
    allowed_domains = ['kagle.com']
    start_urls = ['http://kagle.com/']

    def parse(self, response):
        pass
