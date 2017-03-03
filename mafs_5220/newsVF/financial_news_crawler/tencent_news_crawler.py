# coding=utf-8

from bs4 import BeautifulSoup
import urllib.request
import News
import json
import re
import demjson
import time
from datetime import datetime
from prewash_tags import remove_tags
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
                article.source = "腾讯" + py_data['site_cname']
                article.success = True
                break

        # get the content of the article
        tag = soup.body.find("div", id="Cnt-Main-Article-QQ", bosszone="content")
        # print(tag.attrs)
        article.content = remove_tags(repr(tag))
        # print('here')
        # print(article.content)
        store_article(article)
        return article
    except:
        get_kuaibao_news(url)


def get_content_news(url):
    try:
        # print('here')
        html = urllib.request.urlopen(url).read()
        html = html.decode('gb2312', 'ignore')
        soup = BeautifulSoup(html, "html.parser")
        # find and prewash the content of article
        tag = soup.body.find("div", id="Cnt-Main-Article-QQ", bosszone="content")
        # print(tag)
        if tag is []:
            content = 'NO CONTENT'
        else:
            content = remove_tags(repr(tag))
            # print(content)
        # find and prewash the source of article
        data = soup.body.find('span', bosszone="jgname")
        source = remove_tags(repr(data))
        return (source, content)
    except:
        print('error')
        store_error_url(url)


def get_kuaibao_news(url):
    try:
        js_url = "http://ifzq.gtimg.cn/appstock/news/newsContent/content?{}"
        re_id = re.compile('id=kuaibao-\w+')
        id_news = re_id.findall(url)
        # print(js_url.format(id_news[0]))

        html = urllib.request.urlopen(js_url.format(id_news[0])).read()
        html = html.decode('utf-8')
        # print(html)
        js = json.loads(html)
        # print(js)

        source = js['data']['src']
        # print('source')
        content = ''
        for data in js['data']['formatContent']:
            # print(data['desc'])
            content += remove_tags(data['desc']) + '\r\n'
        # print(content)
        if content == '':
            content = "NO CONTENT"
        return (source, content)
    except:
        print('error')
        store_error_url(url)


def load_article(js_data):
    # print(js_data)
    article = News.News()
    article.url = js_data['url']
    article.title = js_data['title']
    article.newsid = js_data['uid']
    article.pubdate = js_data['datetime']
    if "kuaibao" in article.url:
        (article.source, article.content) = get_kuaibao_news(article.url)
    else:
        (article.source, article.content) = get_content_news(article.url)
    store_article(article)


def get_company_news(code='sh600000',                    # the company's code
                     start_date=datetime(2017, 12, 31),  # the datetime object
                     end_date=datetime(2016, 1, 1)       # the datetime object
                     ):
    """Return the number of news for the given company."""
    date_format = '%Y-%m-%d %H:%M:%S'
    js_url = "http://news2.gtimg.cn/lishinews.php?name=\
              finance_news&symbol=" + code + "&"
    page_number = 1
    page = "page={}&"
    max_number = 30  # update the max number after getting the url
    t = "_du_r_t={}"
    url_page = js_url + page.format(1) + t.format(time.time())

    end = False
    number_of_news = 0
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
                number_of_news += 1
        if end:
            break
        print('finish: stock {} page{}'.format(code, page_number))
        page_number += 1
        url_page = js_url + page.format(page_number) + t.format(time.time())
    print('finish: ', code)
    return number_of_news


# print(get_company_news('sz000001'))
# url = "http://stock.qq.com/a/20170210/003454.htm"
# print(get_content_news(url))
# print(get_kuaibao_news(url))
# print('end')
