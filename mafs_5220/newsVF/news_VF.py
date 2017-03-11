# coding = utf-8
import data_load.crawlerload as cl
import data_analysis as da

companies = ['sh600001','sz000001']

cl.news_load(companies)
cl.stock_load(companies)