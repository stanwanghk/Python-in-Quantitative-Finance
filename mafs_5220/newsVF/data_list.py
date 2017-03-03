'''Saving the companies list and the start and end date that we want to crawling'''
# coding=utf-8
import sqlite3
from datetime import datetime

startdate = datetime.date(datetime.today())
enddate = datetime(2016, 1, 1)
company_list = ['sz000001', ['sz000002']]


def get_date():
    return (startdate, enddate)


def get_company_list():
    return company_list