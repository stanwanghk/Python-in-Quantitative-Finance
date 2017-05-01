import pandas as pd
import read_data as rd


home_path = '/home/stan_wp/Documents/data/output/'
def response_fun(data,l_range=range(501)):
    # data = rd.read_data()
    res = []
    dates = data.index
    dates = dates.drop_duplicates()
    for l in l_range:
        num = 0
        ave = 0.0
        for date in dates:
            raw = data[data.index==date]
            lag_data = raw[['Index','VWAP','Time']].set_index(keys='Index')
            raw = raw.assign(lag=l)
            raw['Index'] += raw['lag']
            t_data=raw[['Index','midQ','Sign','Time']].set_index(keys='Index')
            responsed = lag_data.join(t_data,rsuffix='_t')
            responsed = responsed.dropna()
            responsed['influence'] = (responsed.VWAP-responsed.midQ)*responsed.Sign
            ave = (ave*num+responsed.influence.sum())/(num+len(responsed.influence))
            num += len(responsed.influence)
        res.append(ave)
        # print('finish: ', l)
    # file = open(home_path+"Q2.csv",'w')
    # for j in range(len(res)):
    #     file.write('{},{}\n'.format(j,res[j]))
    # file.close()
    return res