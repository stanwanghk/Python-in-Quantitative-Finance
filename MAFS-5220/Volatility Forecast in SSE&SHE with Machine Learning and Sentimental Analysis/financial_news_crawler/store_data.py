# coding=utf-8
import sqlite3


db_name = 'VF_SSE_SHE.sqlite'
f_name = 'error.txt'


def store_article(article):
    content_file = open('article.txt', 'a')
    content_file.write('\r\n' + '*'*20)
    content_file.write(article.title+'  ' + article.pubdate + '\r\n')
    content_file.write(article.newsid + '\r\n')
    content_file.write(article.url + '\r\n')
    content_file.write(article.content)
    content_file.write('\r\n')
    content_file.close()


def store_error_url(url):
    error_file = open('../'+f_name, 'a')
    error_file.write(url)
    error_file.write('\r\n')
    error_file.close()
