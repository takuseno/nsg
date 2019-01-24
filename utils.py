import requests
import bs4
import time


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
    google_url = 'https://www.google.co.jp/search'
    # to avoid bot detection
    time.sleep(3.0)
    response = requests.get(google_url, params={'q': query})
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    href = soup.select('.r > a')[0].get('href')
    if href.find('search?q=') > -1:
        href = soup.select('.r > a')[1].get('href')
    return href.replace('/url?q=', '')

def clean_url(url):
    end_index = url.find('&')
    if end_index > -1:
        return url[:end_index]
    return url

def get_original_link(url):
    if url.find('news.yahoo.co.jp/pickup') > -1:
        url = get_article_link(url)
    title, site = get_title_and_url(url)
    original_url = get_top_google_search_link(title, site)
    return clean_url(original_url)
