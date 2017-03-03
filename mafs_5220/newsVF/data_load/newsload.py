# coding=utf-8
import sqlite3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import settings
import data_list
from financial_news_crawler import tencent_news_crawler as tc

def news_load():
    conn = sqlite3.connect(settings.get_sqlite_path())
    cur = conn.cursor()

    cur.execute('''
        DROP TABLE IF EXISTS News''')
    cur.execute('''
        DROP TABLE IF EXISTS Source''')
    cur.execute('''
        CREATE TABLE News (code_id INTEGER, news_id TEXT, pubdate TEXT, url TEXT, \
        title TEXT, source_id INTEGER, content TEXT)
        ''')
    cur.execute('''
        CREATE TABLE Source (id INTEGER, source TEXT)''')

    companies = data_list.get_company_list()
    (start_date, end_date) = data_list.get_date()
    number_of_news = []

    for company in companies:
        number_of_news.append(company, tc.get_company_news(company, start_date, end_date))

    file = settings.get_number_path()
    f = open(file, 'w')
    for number in number_of_news:
        f.write(number, '\r\n')

    f.close()
    print('news loading end')

