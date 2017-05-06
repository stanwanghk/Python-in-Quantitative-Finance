import pandas as pd


home_path = "C:/Users/WPISH/OneDrive/MSc/A_Courses/Spring_Term/MAFS_6010G/homework/Assignment#3/"


def read_data(month='201607'):
    """Return the month data"""
    # form = '%Y%m%d %H%M%S%f'
    form = '%Y%m%d'
    dateparse = lambda x : pd.datetime.strptime(x,form)
    data = pd.read_csv(home_path+'pp1_md_{}_{}.csv'.format(month,month), \
        parse_dates=['Date'], date_parser=dateparse)
    names = data.columns.tolist()
    names[0] = 'Index'
    data.columns = names
    return data


def read_all():
    data = read_data()
    data = data.append(read_data('201608'))
    data = data[(data.BP1!=0)&(data.SP1!=0)]
    # reindex
    dates = data.Date
    dates = dates.drop_duplicates()
    for date in dates:
        length=len(data[data.Date==date])
        data.loc[data.Date==date,['Index']] = range(1,length+1)
    return data
