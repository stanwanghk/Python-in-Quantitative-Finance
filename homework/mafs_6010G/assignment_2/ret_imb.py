import read_data as rd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression as LR


def process_one(origin,tau='5T'):
    # origin = rd.combine_one()
    # convert B,S to 1,-1 respectively
    replace_dict = {'BS': {'S': -1, 'B': 1, ' ': 0}}
    raw = origin.replace(replace_dict)
    raw = raw[raw.BS != 0]
    # normalize Vi by its first moment
    raw['ntrade'] = raw['ntrade'] / raw.ntrade.mean()
    # create a new column imb mid wmid
    raw = raw.assign(imb=lambda x: x.BS * x.ntrade)
    raw = raw.assign(mid=lambda x: (x.AskPrice1 + x.BidPrice1)/2)
    raw = raw.assign(wmid=lambda x: (x.AskPrice1 * x.BidVolume1 + x.BidPrice1 * x.AskVolume1) / (x.BidVolume1 + x.AskVolume1))
    # downsampling
    dsample = pd.DataFrame()
    raw = raw[raw.wmid != float('Inf')]
    price=['mid','wmid','price']
    dsample = raw[price].resample(tau).first()
    dsample['imb'] = raw['imb'].resample(tau).sum()
    dsample = dsample.dropna()
    # get return
    dsample = dsample[dsample.wmid != 0.0]
    dsample['ret'] = dsample.wmid.pct_change()
    dsample = dsample.dropna()
    # dsample = dsample[dsample.ret != -1]
    return dsample


def process_all(code='600519',tau='5T'):
    tdata = pd.DataFrame()
    trade_date = rd.get_trade_date(code)
    for date in trade_date:
        if not(date == '20130902' and code=='600519'):
            odata = rd.combine_one(code,date)
            tdata = tdata.append(process_one(odata,tau))
            print('finish{}'.format(date))
    sigma_ret = tdata.ret.std()
    tdata = tdata[tdata.ret != 0.0]
    # divide to positive_part and negative_part
    pos = tdata.where(tdata.imb>0).dropna()
    neg = tdata.where(tdata.imb<0).dropna()
    pos['lnimb'] = np.log(pos.imb)
    pos['lnret'] = np.log(pos.ret.abs())
    neg['lnimb'] = np.log(neg.imb.abs())
    neg['lnret'] = np.log(neg.ret.abs())
    return pos,neg,sigma_ret


def draw(pos,neg,sigma):
    # plt.scatter(pos['imb'].abs(),pos['ret'].abs()/sigma)
    # plt.scatter(neg['imb'].abs(),neg['ret'].abs()/sigma)
    plt.scatter(pos['lnimb'],pos['lnret'])
    plt.scatter(neg['lnimb'],neg['lnret'])
    plt.show()


def estimation(data,sigma):
    x = data[['lnimb']]
    y = data[['lnret']]
    linreg = LR()
    linreg.fit(x,y)
    gamma = linreg.coef_[0][0]
    beta = linreg.intercept_[0]
    beta = np.exp(beta)/sigma
    return gamma,beta
