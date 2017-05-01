import pandas as pd


home_path = '/home/stan_wp/Documents/data/'


def read_data(month='201607'):
    """Return the month data"""
    # form = '%Y%m%d %H%M%S%f'
    form = '%Y%m%d'
    dateparse = lambda x : pd.datetime.strptime(x,form)
    data = pd.read_csv(home_path+'pp1_md_{}_{}.csv'.format(month,month), \
        parse_dates=['Date'], date_parser=dateparse, index_col='Date')
    names = data.columns.tolist()
    names[0] = 'Index'
    data.columns = names
    return data
