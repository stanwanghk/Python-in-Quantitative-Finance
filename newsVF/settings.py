"""setting the saving data file's path."""
# coding=utf-8
from datetime import datetime

home_path = '/home/stan_wp/newsVF/'
# show where to store data
sqlite_path = 'data/VF.sqlite'
error_path = 'data/error.txt'
article_path = 'data/article.txt'
number_path = 'data/numberOfNews.csv'
sample_path = 'data/sample.txt'

# show where to get related data
SHE_path = 'source/SHE.csv'
SHE_sample = 'source/SHE_sample.csv'
SSE_path = 'source/SSE.csv'
SSE_sample = 'source/SSE_sample.csv'
adv_path = 'source/adv.txt'
HowNet = 'source/HowNet/'

# time setting
startdate = datetime(2017, 1, 1)
enddate = datetime(2016, 1, 1)
time_format = "%Y-%m-%d"


def get_article_path():
    """"Return the test article path."""
    return home_path + article_path


def get_sqlite_path():
    """Return the Database path."""
    return home_path + sqlite_path


def get_error_path():
    """"Return the file's path,which contains the error url."""
    return home_path + error_path


def get_number_path():
    """"Return the file that saves the number of news for given company."""
    return home_path + number_path


def get_exchange_path():
    return home_path + SHE_path, home_path + SSE_path


def get_sample_data():
    return home_path + SSE_sample, home_path + SHE_sample

def get_date():
    return (startdate, enddate)


def get_time_format():
    return time_format


def get_adv_path():
    return home_path + adv_path;


def get_sample_path():
    return home_path + sample_path

def get_sentiment_files(name):
    fname={}
    fname['positive'] = '正面情感词语（中文）.txt'
    fname['negative'] = '负面情感词语（中文）.txt'
    fname['level'] = '程度级别词语（中文）.txt'
    fname['argue'] = '主张词语（中文）.txt'
    fname['support'] = '正面评价词语（中文）.txt'
    fname['object'] = '负面评价词语（中文）.txt'
    return home_path + HowNet + fname[name]

