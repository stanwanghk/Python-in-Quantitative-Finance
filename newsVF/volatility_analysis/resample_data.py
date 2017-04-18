import pandas as pd
import numpy as np
import sqlite3
import settings


def pro_one_code(code='sz000001',return_col=['code','p_var','mean_return','num_news','sum_abs_sent']):
    conn = sqlite3.connect(settings.get_sqlite_path())
    # process the stock
    sql = ''' SELECT  date,close,volume,p_change  FROM Stock 
              WHERE code like {}'''.format('\'' + code + '\'')
    # print(sql)
    raw = pd.read_sql(sql=sql,con=conn,index_col='date')
    # raw = raw[columns]
    raw.index = pd.to_datetime(raw.index)
    draw = pd.DataFrame()
    draw['p_var'] = raw['p_change'].resample('W',label='left').var()
    draw['mean_return'] = raw['p_change'].resample('W',label='left').mean()
    draw = draw.assign(code=code)

    # process the news
    sql_news = '''  SELECT pubdate,source_id,sentiment FROM News LEFT OUTER JOIN Company_News 
                    ON News.id=Company_News.news_table_id
                    WHERE Company_News.company_id like {}'''.format('\'' + code + '\'')
    raw_news = pd.read_sql(sql=sql_news, con=conn, index_col = 'pubdate')
    raw_news.index = pd.to_datetime(raw_news.index)
    raw_news['abs_sentiment'] = raw_news.sentiment.abs()
    draw_news = pd.DataFrame()
    draw_news['sum_abs_sent'] = raw_news['abs_sentiment'].resample('W',label='left').sum()
    draw_news['num_news'] = raw_news['sentiment'].resample('W',label='left').count()
    # fill the NaN with 0 for news
    draw = draw.join(draw_news)
    draw[['sum_abs_sent','num_news']] = draw[['sum_abs_sent','num_news']].fillna(0)
    # drop the NaN when the stock is not exchanged
    draw = draw.dropna()
    return draw[return_col]


def pro_all_codes():
    sample_path = settings.get_sample_path()
    home_path = settings.get_home_path()
    f = open(sample_path)
    raw = pd.DataFrame()
    for line in f:
        line = line.split(',')
        one_data = pro_one_code(line[0])
        raw = raw.append(one_data)
        one_data.to_csv(home_path + 'data/week_data/{}.csv'.format(line[0]))
        print('finish {}'.format(line[0]))
    raw.to_csv(home_path + 'data/week_data/total.csv')
    return raw
    