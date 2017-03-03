# coding=utf-8
import sqlite3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import settings


def store_article(article):
    article_path = settings.get_article_path()
    content_file = open(article_path, 'a')
    content_file.write('\r\n' + '*' * 20)
    content_file.write('\r\n' + article.title + '  ' + article.pubdate + '\r\n')
    # content_file.write(article.source + '\r\n')
    content_file.write(article.newsid + '\r\n')
    content_file.write(article.url + '\r\n')
    if article.content is not None:
        content_file.write(article.content)
    content_file.write('\r\n')
    content_file.close()


def store_error_url(url):
    error_path = settings.get_error_path()
    error_file = open(error_path, 'a')
    error_file.write(url)
    error_file.write('\r\n')
    error_file.close()
