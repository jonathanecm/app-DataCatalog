# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import pymongo
from scrapy.exceptions import IgnoreRequest
from scrapy import signals


'''
------------------------------------------------------------
Downloader Middlewares
------------------------------------------------------------
'''
#--Create random user agent
class RandomUserAgentMiddleware(object):
    
    #Acquire user agent candidates in 'settings.py'
    @classmethod
    def from_crawler(cls, crawler):
        cls.candidates = crawler.settings['USERAGENT_CANDIDATES']
        return cls(settings)
    
    #Randomly select one from the candidates and update request header
    def process_request(self, request, spider):
        ua = random.choice(self.candidates)
        request.headers['User-Agent'] = ua


#--Detect duplicate record by comparing with the dataset id already in the 'Kaggle_Main' collection
class DuplicateDetectorMiddleware(object):

    #Acquire the dataset id in the collection
    @classmethod
    def from_crawler(cls, crawler):
        mongo_uri=crawler.settings.get('MONGO_URI'),
        mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        client = pymongo.MongoClient(crawler.settings.get('MONGO_URI'))
        db = client[crawler.settings.get('MONGO_DATABASE', 'items')]
        result = db['Kaggle_Main'].find({}, {
                '_id': False,
                'datasetId': True
            })
        cls.ids = [item['datasetId'] for item in list(result)]        
        return cls()
    
    #If exists, drop the request by raising a special error
    def process_request(self, request, spider):
        if 'datasetId' in request.meta.keys():
            if request.meta['datasetId'] in self.ids:

                #This type of error, if not specifically handled, will be ignored by the spider
                raise IgnoreRequest()
        



'''
------------------------------------------------------------
Middleware Templates
------------------------------------------------------------
'''
class ScraperSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ScraperDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
