import requests
import bs4


def get_redirect_url(url):
    response = requests.get(url)
    return response.url

def get_title_and_url(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    cobrand_url = soup.select('.ynCobrandBanner > a')[0].get('href')
    title = soup.select('.hd > h1')[0].get_text()
    return title, get_redirect_url(cobrand_url)

def get_top_google_search_link(title, site):
    query = title + ' site:' + site
    google_url = 'https://www.google.co.jp/search'
    response = requests.get(google_url, params={'q': query})
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    return soup.select('.r > a')[0].get('href').replace('/url?q=', '')

def get_original_link(url):
    title, site = get_title_and_url(url)
    return get_top_google_search_link(title, site)

title, url = get_title_and_url('https://headlines.yahoo.co.jp/article?a=20190122-00010006-kaiyou-ent')
