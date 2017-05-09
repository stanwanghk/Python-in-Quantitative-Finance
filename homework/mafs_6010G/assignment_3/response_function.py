import pandas as pd
import read_data as rd
import matplotlib.pyplot as plt


home_path = "C:/Users/WPISH/OneDrive/MSc/A_Courses/Spring_Term/MAFS_6010G/homework/Assignment#3/output/"


def response_group(raw,l_range=range(501),path=None):
    res = {}
    for l in l_range:
        data = raw.copy()
        data.loc[:,['VWAP','date_lag']] = data[['VWAP','date_lag']].shift(-l)
        responsed = data[(data.group==1)&(data.Date==data.date_lag)].dropna().copy()
        responsed['influence'] = (responsed.VWAP-responsed.midQ)*responsed.Sign / (responsed.SP1-responsed.BP1)
        res[l] = responsed.influence.mean()
        if (l%100==0):
            print("finish: ",l)
    file = open(path,'w')
    for j in range(len(res)):
        file.write('{},{}\n'.format(j,res[j]))
    file.close()


def response_all(data,l_range=range(1,501),save=False):
    # data = data[(data.BP1!=0)&(data.SP1!=0)]
    data['date_lag'] = data.Date
    res = {}
    for l in l_range:
        data.loc[:,['VWAP','date_lag']] = data[['VWAP','date_lag']].shift(-1)
        responsed = data[(data.group==1)&(data.Date==data.date_lag)].dropna().copy()
        responsed['influence'] = (responsed.VWAP-responsed.midQ)*responsed.Sign / (responsed.SP1-responsed.BP1)
        res[l] = responsed.influence.mean()
        if (l%100==0):
            print("finish: ",l)
    if save:
        file = open(home_path+"Q2.csv",'w')
        for j in range(len(res)):
            file.write('{},{}\n'.format(j,res[j]))
        file.close()
    return res


def plot_q2():
    data = pd.read_csv(home_path+"Q2.csv",header=None)
    data.columns = ['l','R_l']
    plt.figure(figsize=(15,5),dpi=70)
    plt.plot(data.l,data.R_l,':')
    plt.xlim(xmin=-20,xmax=520)
    # plt.ylim(ymin=0.15,ymax=1.0)
    plt.xlabel("Lag")
    plt.ylabel("Response function bechmarked to prevailing mid quote")
    plt.title("Response fuction(in the unit of bid-ask spread of prevailing quote)")
    plt.show()
    # return data
