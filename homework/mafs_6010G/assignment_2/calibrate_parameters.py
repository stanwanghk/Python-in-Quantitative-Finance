import read_data as rd
import numpy as np
import datetime
import os
import re


except_date=[datetime.datetime(2013,2,18,9,25,0),datetime.datetime(2013,2,18,9,30,0),
            datetime.datetime(2013,2,18,9,35,0),datetime.datetime(2013,6,17,13,0,0)]

def isValid(date):
    if date in except_date:
        return False
    tdate = date.strftime("%Y%m%d")
    trade_date = rd.get_trade_date()
    if tdate in trade_date:
        morning_start = datetime.datetime.strptime(tdate + " 09:25:00", "%Y%m%d %H:%M:%S")
        morning_end = datetime.datetime.strptime(tdate + " 11:30:00", "%Y%m%d %H:%M:%S")
        afternoon_start = datetime.datetime.strptime(tdate + " 13:00:00", "%Y%m%d %H:%M:%S")
        afternoon_end = datetime.datetime.strptime(tdate + " 15:00:00", "%Y%m%d %H:%M:%S")
        if (date < morning_end and date >= morning_start) or (date<afternoon_end and date >= afternoon_start):
            return True
        else:
            return False
        # hour = date.hour
        # mins = date.minute
        # if((hour == 9 and mins >= 25) or (hour == 10) or (hour == 11 and mins < 30)) or (hour > 12 and hour < 15):
        #     return True
        # else:
        #     return False
    else:
        return False


def parameters(origin,tao='5min'):
    # origin = rd.read_all_files()

    # resample the data
    # convert B,S to 1,-1 respectively
    replace_dict = {'BS': {'S': -1, 'B': 1, ' ': 0}}
    raw = origin.replace(replace_dict)
    # normalize Vi by its first moment
    raw['ntrade'] = raw['ntrade'] / raw.ntrade.mean()
    # create a new column imb
    raw = raw.assign(imb=lambda x: x.BS * x.ntrade)
    # downsampling with given tau
    resample_raw = raw['imb'].resample(tao,label='left').agg({'number': np.size, 'imb': np.sum})
    # drop the data whose time is from 11:30-13:00
    resample_raw = resample_raw.select(isValid)

    # calibrate the parameters
    ns, nb, nan = origin['BS'].value_counts()
    prob = nb / (ns + nb)
    print('probability: ', prob)

    lamb = resample_raw['number'].mean()
    print('lambda: ', lamb)
    imb_mean = resample_raw['imb'].mean()
    imb_var = resample_raw['imb'].var()
    print(imb_mean, imb_var)

    return resample_raw


def rou(data,number=1000):
    # data = raw['BS']
    corr = []
    x = []
    for i in range(1,number+1):
        corr.append(np.log(data.autocorr(i)))
        x.append(i)
    return corr,x

