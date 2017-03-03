#coding = utf-8
import sqlite3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import settings
import data_list
from stock_crawler import yahoo_finance as yf


def stock_load():
    conn = sqlite3.connect(settings.get_sqlite_path())
    cur = conn.cursor()

    cur.execute('''
        DROP TABLE IF EXISTS Stock''')
    cur.execute('''
        CREATE TABLE Stock (code_id INTEGER, price_id INTEGER,trading_date TEXT, closing_price INTEGER, volumn INTEGER)
        ''')

    companies = data_list.get_company_list()
    (start_date, end_date) = data_list.get_date()

    for company in companies:
        yf.get_company_stock(company, start_date, end_date)

    print('stocks loading end')
