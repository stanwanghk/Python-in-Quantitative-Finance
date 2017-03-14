# coding = utf-8
import data_load as dl
import settings
import sqlite3


dl.reset_sqlite()
dl.company_list_load()

conn = sqlite3.connect(settings.get_sqlite_path())
cur = conn.cursor()
cur.execute(''' SELECT code FROM Companies''')
raws = cur.fetchall()
companies = []
for raw in raws:
    companies.append(raw[0])
# print(companies)

dl.news_load(companies)

dl.stock_load(companies)