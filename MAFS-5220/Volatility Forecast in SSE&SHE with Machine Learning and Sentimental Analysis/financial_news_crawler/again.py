# coding=utf-8

from bs4 import BeautifulSoup
import News
from news_crawler import filter_tags
import urllib.request
import zlib


def function(url):
    try:
        # html = open(url, encoding='gbk')
        req = urllib.request.Request(url)
        req.add_header('Accept-encoding', 'gzip')
        # if not (refer is None):
        #    req.add_header('Referer', refer)
        html = urllib.request.urlopen(req, timeout=120)
        rawdata = html.read()
        gzipped = html.headers.get('Content-Encoding')
        if gzipped:
            rawdata = zlib.decompress(rawdata, 16+zlib.MAX_WBITS)
        print('here')
        rawdata = rawdata.decode('gbk')
        # print(rawdata)
        soup = BeautifulSoup(rawdata, 'html.parser')
        # print(soup)
        article = News.News()
        article.url = url
        title = soup.head.title.get_text()
        article.title = title
        article.newsid = 0  # will be given when stored in SQlite
        # get the description
        source = soup.body.find(id="news_source")
        article.source = source.get_text()
        time = soup.body.find(id="news_time")
        article.pubdate = time.get_text()
        # get the content
        content = soup.body.find(id="news_text")
        if content is not None:
            article.content = filter_tags(repr(content.get_text()))
        return article
    except:
        print('error:', url)
        error_url.add(url)

error_url = set()
url = r'http://finance.qq.com/products/portfolio/news_zixuangu.htm?id=kuaibao-20170213C07E9200&s=w&from=web&r'

print('end')