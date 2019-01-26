import requests
import bs4
import time
import logging

from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


def get_redirect_url(url):
    response = requests.get(url)
    return response.url

def get_article_link(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    return soup.select('.newsLink')[0].get('href')

def get_title_and_url(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    cobrand_url = soup.select('.ynCobrandBanner > a')[0].get('href')
    title = soup.select('.hd > h1')[0].get_text()
    return title, get_redirect_url(cobrand_url)

def get_top_google_search_link(title, site):
    query = title + ' site:' + site
    # use headless browser to avoid bot detection
    driver = webdriver.PhantomJS()
    # google search
    driver.get('https://www.google.co.jp?pws=0')
    driver.find_element_by_name('q').send_keys(query)
    driver.find_element_by_name('q').send_keys(Keys.RETURN)
    # check bot detection
    LOGGER.debug(driver.current_url)
    if driver.current_url.find('www.google.com/sorry/index') > -1:
        raise Exception('we are detected as a bot by Google now. Go to <a href="{}">here</a>.'.format(url))
    # get the first result
    links = driver.find_elements_by_css_selector('h3 > a')
    url = links[0].get_attribute('href')
    if url.find('/search?q=') > -1:
        url = links[1].get_attribute('href')
    # release
    driver.quit()
    return clean_url(url)

def clean_url(url):
    end_index = url.find('&')
    if end_index > -1:
        url = url[:end_index]
    return url.replace('https://www.google.co.jp', '').replace('/url?q=', '')

def get_original_link(url):
    if url.find('news.yahoo.co.jp/pickup') > -1:
        url = get_article_link(url)
    title, site = get_title_and_url(url)
    return get_top_google_search_link(title, site)
