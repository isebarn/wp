from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import os
from pprint import pprint
from time import sleep

def run_selenium_with_scanwp():
  URL = 'https://scanwp.net'
  driver = webdriver.Remote(os.environ.get('BROWSER'), DesiredCapabilities.FIREFOX)
  #driver.implicitly_wait(10) # seconds
  driver.get(URL)

  sites = read_file('testsites.txt')

  results = []
  for site in sites[0:10]:
    try:
      input = driver.find_element_by_id('url')
      input.clear()
      input.send_keys(site)
      button = driver.find_element_by_xpath("//button[@type='submit']")
      button.click()

      plugin_divs = driver.find_elements_by_xpath("//div[@class='plugin-title']/a")
      plugins = [x.text for x in plugin_divs]

      result = {}
      result['site'] = site
      result['plugins'] = plugins
      results.append(result)

    except Exception as e:
      print("Error with: {}".format(site))

  driver.close()

  return results

def run_selenium_with_wpdetector():
  URL = 'https://wpdetector.com/'
  driver = webdriver.Remote(os.environ.get('BROWSER'), DesiredCapabilities.FIREFOX)
  #driver.implicitly_wait(10) # seconds
  driver.get(URL)

  sites = read_file('sites.txt')
  results = []

  for site in sites[0:3]:
    result = {}
    result['site'] = site
    result['wordpress'] = False
    result['plugins'] = []

    try:
      # wait for loading to finish
      loader = driver.find_element_by_id('loading')
      while 'block' in loader.get_attribute('style'):
        print('wait')
        sleep(1)

      sleep(1)

      input = driver.find_element_by_id('search_data')
      input.clear()
      input.send_keys(site)
      input.send_keys(Keys.ENTER)

      while 'block' in loader.get_attribute('style'):
        sleep(1)


      result_div = driver.find_element_by_id('results')

      # This indicates it's a WP site
      if 'Great News!' in result_div.text:
        result['wordpress'] = True

        # get plugin names
        plugin_divs = driver.find_elements_by_xpath("//div[@class='plug_in_card']")

        plugins = []
        for plugin_div in plugin_divs:
          plugin = {}
          plugin['title'] = plugin_div.find_element_by_xpath(".//div[@class='plugin_title']").text

          try:
            plugin['url'] = plugin_div.find_element_by_xpath(".//a").get_attribute('href')

          except NoSuchElementException as e:
            plugin['url'] = ''

          plugins.append(plugin)


        result['plugins'] = plugins

      # This indicates it's not a WP site
      elif 'Unfortunately' in result_div.text:
        pass

      results.append(result)

    except Exception as e:
      print(e)


  driver.close()
  return results


def read_file(filename):
  file = open(filename, "r")
  return file.readlines()

if __name__ == '__main__':
  pprint(run_selenium_with_wpdetector())
