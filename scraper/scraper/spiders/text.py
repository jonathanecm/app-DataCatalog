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
            request = scrapy.Request(url=link, callback=self.parse_main)
            request.meta['id'] = '1rr'
            yield request
           
    def parse_main(self, response):
        targetPath = '//p/parent::*'
        paragraphs = response.selector.xpath(targetPath).extract()
        text = '\n'.join(paragraphs)

        with open('../data/some.txt', 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)

        # with open('some.csv', 'a', newline='', encoding='utf-8') as f:
        #     writer = csv.writer(f)
        #     writer.writerow([response.meta['id'], text])


with open('./data/some.txt', 'r', encoding='utf-8') as f:
    text = f.read()

def unique(list_in): 
    #Initialize an empty list
    list_out = [] 
      
    #Traverse all elements, check if exists
    for i in list_in: 
        if i not in list_out: list_out.append(x)
            
    return list_out

#'pixnet.net'
from lxml import etree
doc = etree.HTML(text)
finder = etree.XPath('//*[@class="article-content-inner"]/descendant::p/descendant::text()')
result = unique(finder(doc))

for i in result:
    if i.strip() != '': print(i.strip())
    print(etree.tostring(i, pretty_print=True, method="html", encoding='unicode'))