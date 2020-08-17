import scrapy
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from time import time
from pprint import pprint
import os
import re

try:
  from ORM import Operations

except Exception as e:
  from wp.spiders.ORM import Operations

class PluginSpider(scrapy.Spider):
  name = "plugin"

  def start_requests(self):
    start_urls = []

    for url in start_urls:
      yield scrapy.Request(url=url,
        callback=self.parser,
        errback=self.errbacktest,
        meta={'root': url})

  def parser(self, response):
    #response.meta.get('root')
    pass

  def errbacktest(self, failiure):
    pass

  @classmethod
  def from_crawler(cls, crawler, *args, **kwargs):
    spider = super().from_crawler(crawler, *args, **kwargs)
    crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
    return spider

  def spider_closed(self, spider):
    pass

if __name__ == "__main__":
  pass