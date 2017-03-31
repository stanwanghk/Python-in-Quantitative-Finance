import pandas as pd
import os 
import re

home_path = '/home/stan_wp/Documents/data/'
path = home_path + '/SH601398/'
files = os.listdir(path)
re_date = re.compile(r'\d{8}')
trade_date = []
for file in files:
    if 'trade' in file:
        temp_date = re_date.findall(file)[0]
        trade_date.append(temp_date)


def read_all_files(file_type='trade',code='600519'):
    raw = pd.DataFrame()
    for date in trade_date:
        raw = raw.append(read_one_file(file_type,code,date))
        print('finished {}'.format(date))
    return raw


def read_one_file(file_type='trade',code='600519',tdate='20130104'):
    path = home_path + 'SH{}/'.format(code)
    file = '{}_SH_{}_{}.csv'.format(file_type,code,tdate)
    path = path+file
    if file_type == 'trade':
        form = '%Y%m%d %H%M%S%f'
    else:
        form = '%Y%m%d %H%M%S'
    dateparse = lambda x : pd.datetime.strptime(x,form)
    raw = pd.read_csv(path,parse_dates=[['date','time']],date_parser=dateparse,index_col='date_time')
    return raw


def combine_one(code='600519', tdate='20130104'):
    raw_trade = read_one_file('trade', code, tdate)
    raw_quote = read_one_file('quote', code, tdate)
    ask_bid = ['AskPrice1', 'AskVolume1', 'BidPrice1', 'BidVolume1']
    outer = raw_trade.join(raw_quote[ask_bid], how='outer')
    outer = outer[ask_bid]
    outer = outer.fillna(method='ffill')
    output = raw_trade.join(outer)
    output = output.drop_duplicates()
    return output


def combine_all(code='600519'):
    output = pd.DataFrame()
    for date in trade_date:
        # print(date)
        raw = combine_one(code, date)
        output = output.append(raw)
        print('finish {}'.format(date))
    return output
