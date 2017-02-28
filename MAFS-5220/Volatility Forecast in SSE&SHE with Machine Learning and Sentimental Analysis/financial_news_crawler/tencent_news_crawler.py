# coding=utf-8

from bs4 import BeautifulSoup
import urllib.request
import News
import json
import re
import demjson
import time
from datetime import datetime
from prewash_tags import filter_tags
from store_data import store_article, store_error_url


def get_qq_news(url):
    try:
        html = urllib.request.urlopen(url).read()
        html = html.decode('gb2312', 'ignore')
        soup = BeautifulSoup(html, "html.parser")

        # define a new object of news
        article = News.News()
        article.url = url
        # get the related information, i.e title, pubtime...
        tags = soup.head.find_all(type="text/javascript")
        re_content = re.compile('{.+title.+}', re.DOTALL)
        for tag in tags:
            js_data = repr(tag.get_text)
            # print(js_data)
            js_data = re.findall(re_content, js_data)
            if len(js_data) is 1:
                py_data = demjson.decode(js_data[0])
                article.url = py_data['article_url']
                article.title = py_data['title']
                article.newsid = py_data['id']
                article.pubdate = py_data['pubtime']
                article.source = "腾讯"+py_data['site_cname']
                article.success = True
                break

        # get the content of the article
        tag = soup.body.find(id="Cnt-Main-Article-QQ")
        article.content = filter_tags(repr(tag.get_text()))
        return article.content
    except:
        get_kuaibao_news(url)


def get_content_news(url):
    try:
        html = urllib.request.urlopen(url).read()
        html = html.decode('gb2312', 'ignore')
        soup = BeautifulSoup(html, "html.parser")
        tag = soup.body.find(id="Cnt-Main-Article-QQ")
        if tag is []:
            get_kuaibao_news(url)
        else:
            content = filter_tags(repr(tag.get_text()))
            return content
    except:
        # get_kuaibao_news(url)
        store_error_url(url)


def get_kuaibao_news(url):
    try:
        return article
    except:
        store_error_url(url)


def load_article(js_data):
    article = News.News()
    article.url = js_data['url']
    article.title = js_data['title']
    article.newsid = js_data['uid']
    article.pubdate = js_data['datetime']
    article.content = get_content_news(article.url)
    store_article(article)


def get_company_news(exchange='sh',  # = sz or sh
                     code='600000',  # the company's code
                     start_date=datetime(2017, 12, 31),  # the datetime object
                     end_date=datetime(2016, 12, 1)  # the datetime object
                     ):
    date_format = '%Y-%m-%d %H:%M:%S'
    js_url = "http://news2.gtimg.cn/lishinews.php?name=\
              finance_news&symbol="+exchange+code+"&"
    page_number = 1
    page = "page={}&"
    max_number = 2  # update the max number after getting the url
    t = "_du_r_t={}"
    url_page = js_url + page.format(1)+t.format(time.time())

    end = False
    while page_number < max_number:
        rawdata = urllib.request.urlopen(url_page).read()
        rawdata = rawdata.decode('unicode-escape')
        # print(type(rawdata))
        re_content = re.compile('{.+code.+}', re.DOTALL)
        rawdata = re_content.findall(rawdata)
        json_data = rawdata[0]
        js = json.loads(json_data)
        for data in js['data']['data']:
            news_time = datetime.strptime(data['datetime'], date_format)
            # print(news_time)
            if news_time <= end_date:
                end = True
                break
            if news_time <= start_date:
                load_article(data)
        if end:
            break
        page_number += 1
        url_page = js_url + page.format(page_number) + t.format(time.time())
    print('finish: ', code)


get_company_news('sz', '000002')

