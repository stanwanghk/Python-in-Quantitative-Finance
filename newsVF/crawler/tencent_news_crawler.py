"""Crawling news for given company in the www.finance.qq.com."""
# coding=utf-8
from bs4 import BeautifulSoup
import urllib.request
import json
import re
import demjson
import time
from datetime import datetime
import crawler.store_news as sn
import crawler.News as News
import crawler.prewash_tags as pt


def get_qq_news(code, url):
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
                article.companyid = code
                break

        # get the content of the article
        tag = soup.body.find("div", id="Cnt-Main-Article-QQ", bosszone="content")
        # print(tag.attrs)
        article.content = pt.remove_tags(repr(tag))
        # print('here')
        sn.store_article_sqlite(article)
        return article
    except:
        print('error: ', url)
        sn.store_error_url(url)


def get_content_news(url, code):
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
            # print(repr(tag))
            content = pt.remove_tags(repr(tag))
            # print(content)
        # find and prewash the source of article
        data = soup.body.find('span', bosszone="jgname")
        source = pt.remove_tags(repr(data))
        return (source, content)
    except:
        print('error: ', url)
        sn.store_error_text(code + ':' + url)


def get_kuaibao_news(url, code):
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
            content += pt.remove_tags(data['desc']) + '\r\n'
        # print(content)
        if content == '':
            content = "NO CONTENT"
        return (source, content)
    except:
        print('error: ', url)
        sn.store_error_text(code + ':' + url)


def load_article(js_data, code):
    # print(js_data)
    article = News.News()
    article.companyid = code
    article.url = js_data['url']
    article.title = js_data['title']
    article.newsid = js_data['uid']
    article.pubdate = js_data['datetime']
    if "kuaibao" in article.url:
        (article.source, article.content) = get_kuaibao_news(article.url, code)
    else:
        (article.source, article.content) = get_content_news(article.url, code)
    sn.store_article_sqlite(article)


def get_company_news(code='sh600000',                    # the company's code
                     start_date=datetime(2017, 12, 31),  # the datetime object
                     end_date=datetime(2016, 1, 1)       # the datetime object
                     ):
    """Return the number of news for the given company."""
    try:
        date_format = '%Y-%m-%d %H:%M:%S'
        js_url = "http://news2.gtimg.cn/lishinews.php?name=finance_news&symbol=" + code + "&"
        page_number = 1
        page = "page={}&"
        max_number = 50  # update the max number after getting the url
        t = "_du_r_t={}"
        url_page = js_url + page.format(page_number) + t.format(time.time())

        end = False
        number_of_news = 0
        while page_number < max_number:
            rawdata = urllib.request.urlopen(url_page).read()
            rawdata = rawdata.decode('unicode-escape')

            re_content = re.compile('^var.*?{')
            json_data = re_content.sub('{', rawdata)
            # print(json_data)

            # to correct the json data when lack of \ or invalid\
            i = 0
            while i <= 100:
                try:
                    i += 1
                    js = json.loads(json_data)   # try to parse...
                    break                    # parsing worked -> exit loop
                except Exception as e:
                    # print(e)
                    # position of unexpected character after '"'
                    unexp = int(re.findall(r'\(char (\d+)\)', str(e))[0])
                    error = str(e)
                    if 'delimiter' in error:
                        # "Expecting , delimiter: line 34 column 54 (char 1158)"
                        # # position of unescaped '"' before that
                        # unesc = json_data.rfind(r'"', 0, unexp)
                        # json_data = json_data[:unesc] + r'\"' + json_data[unesc + 1:]
                        # # position of correspondig closing '"' (+2 for inserted '\')
                        # closg = json_data.find(r'"', unesc + 2)
                        # json_data = json_data[:closg] + r'\"' + json_data[closg + 1:]
                        json_data = json_data[: unexp - 1] + json_data[unexp:]
                    elif 'Invalid' in error:
                        # print("here")
                        # Invalid \escape: line 1 column 8487 (char 8486)
                        json_data = json_data[: unexp] + json_data[unexp + 1:]
            # print(json_data)
            js = json.loads(json_data)
            # print(js)

            for data in js['data']['data']:
                news_time = datetime.strptime(data['datetime'], date_format)
                if news_time <= end_date:
                    end = True
                    break
                if news_time <= start_date:
                    number_of_news += 1
                    load_article(data, code)
            if end:
                break

            print('finish: stock {} page{}'.format(code, page_number))
            page_number += 1
            url_page = js_url + page.format(page_number) + t.format(time.time())
        print('finish: ', code)
        return number_of_news
    except Exception as e:
        print(e, code)
        sn.store_error_text('news loading error: ' + code)
