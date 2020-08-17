import scrapy
from scrapy import signals
from time import time
from pprint import pprint
from scrapy.crawler import CrawlerProcess
import os
import re
import json

try:
  from ORM import Operations
  from Email import Email

except Exception as e:
  from wp.spiders.ORM import Operations
  from wp.spiders.Email import Email


def plugin_name(url):
  try:
    return url.split('wp-content/plugins/')[1].split('/')[0]

  except Exception as e:
    print("Name Error")
    return ''

def plugin_version(url):
  # first attempt to get from ?ver=x.y.z from the end of the url
  version_split = url.split('?ver=')
  if len(version_split) == 2:
    return version_split[1]

  # see if there is something inside the url that resembles a version number
  regex_version = re.findall(r'(?:(\d+\.(?:\d+\.)*\d+))', url)
  if len(regex_version) == 1:
    return regex_version[0]

  return url

class RootSpider(scrapy.Spider):
  name = "root"
  results = []
  plugins = {}
  plugin_url = 'https://wordpress.org/plugins/{}/'

  def read_file(self, filename):
    file = open(filename, "r")
    return file.readlines()

  def start_requests(self):
    self.sites = getattr(self, 'sites', 'sites.txt')

    start_urls = self.read_file('sites.txt')

    for url in start_urls:
      yield scrapy.Request(url=url,
        callback=self.parser,
        errback=self.errbacktest,
        meta={'root': url})

  def parser(self, response):
    plugins = response.xpath("//script/@src").extract()
    plugins = [x for x in plugins if 'wp-content/plugins' in x]
    plugins = { plugin_name(x): plugin_version(x) for x in plugins}

    result = {}
    result['site'] = response.request.url
    result['plugins'] = plugins
    result['wordpress'] = 'wp-content/' in response.text

    self.results.append(result)

    for plugin, version in result['plugins'].items():
      if plugin not in self.plugins:
        yield scrapy.Request(url=self.plugin_url.format(plugin),
          callback=self.plugin_parser,
          errback=self.errbacktest,
          meta={'plugin': plugin})

  def plugin_parser(self, response):
    current_version = response.xpath("//div[@class='entry-meta']/div/ul/li/strong/text()").extract_first()
    plugin = response.meta.get('plugin')
    self.plugins[plugin] = current_version

  def errbacktest(self, failiure):
    pass

  @classmethod
  def from_crawler(cls, crawler, *args, **kwargs):
    spider = super().from_crawler(crawler, *args, **kwargs)
    crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
    return spider

  def spider_closed(self, spider):

    # Save data
    for item in self.results:
      site = Operations.SaveSite(item)
      for plugin, version in item['plugins'].items():
        Operations.SavePlugin(plugin, version, site.Id)

    for plugin, version in self.plugins.items():
      Operations.UpdatePluginVersion({'key': plugin, 'value': version})


    # Logic to determine which plugins are outdated
    plugins = {k: v for k, v in self.plugins.items() if v is not None}

    for site in self.results:
      site['outdated'] = []

      for plugin, version in site['plugins'].items():

        if plugin in plugins and  version < plugins[plugin]:
          site['outdated'].append({'plugin': plugin, 'version': version, 'current': plugins[plugin]})

    # format data for email
    email_data = [{'site': site['site'], 'outdated': site['outdated']} 
      for site in self.results if len(site['outdated']) > 0]

    # write email_data dictionary to file
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(email_data, f, ensure_ascii=False, indent=4)

    # send email
    email = Email({'email': os.environ.get("EMAIL"), 'password': os.environ.get("PASSWORD")})


if __name__ == "__main__":
  results = [{'site': 'https://www.whitehouse.gov', 'plugins': {}}, {'site': 'https://jquery.com', 'plugins': {}}, {'site': 'https://www.plesk.com', 'plugins': {'LayerSlider': '6.9.2', 'reading-progress-bar': '710074f8b82941ee603715288e91a707', 'wp_glossary': '710074f8b82941ee603715288e91a707', 'ajax-search-pro': '0Qt1QS', 'gravityforms': '2.4.20', 'rate-my-post': '3.3.0', 'wp-one-time-file-download': '1.0', 'social-warfare': '4.0.2', 'eventON': '2.6', 'jupiter-donut': '1.0.2', 'js_composer_theme': '6.0.5', 'wp-rocket': '16.1'}}]
  plugins = {'rate-my-post': '3.3.1', 'social-warfare': '4.0.2', 'reading-progress-bar': '1.2.1', 'js_composer_theme': None, 'LayerSlider': None, 'gravityforms': None, 'jupiter-donut': None, 'eventON': None, 'wp-one-time-file-download': None, 'wp-rocket': None, 'wp_glossary': None, 'ajax-search-pro': None}
  plugins = {k: v for k, v in plugins.items() if v is not None}

  for site in results:
    site['outdated'] = []

    for plugin, version in site['plugins'].items():

      if plugin in plugins and  version < plugins[plugin]:
        site['outdated'].append({'plugin': plugin, 'version': version, 'current': plugins[plugin]})


  email_data = [{'site': site['site'], 'outdated': site['outdated']}
    for site in results if len(site['outdated']) > 0]

  with open('data.json', 'w', encoding='utf-8') as f:
      json.dump(email_data, f, ensure_ascii=False, indent=4)

  email = Email({'email': os.environ.get("EMAIL"), 'password': os.environ.get("PASSWORD")})
