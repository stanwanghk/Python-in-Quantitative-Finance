import response_function as rf
import pandas as pd
import matplotlib.pyplot as plt


home_path = "C:/Users/WPISH/OneDrive/MSc/A_Courses/Spring_Term/MAFS_6010G/homework/Assignment#3/output/"


def group_load(raw,group=[0,2,5,10,15,20,30,40,55,90,100000]):
    # data = data[(data.BP1!=0)&(data.SP1!=0)]
    data = raw.copy()
    data = data.assign(group=0)
    data['date_lag'] = data.Date
    for i in range(len(group)-1):
        data.group=0
        data.loc[(data.Size>group[i])&(data.Size<=group[i+1]),'group']=1
        path=home_path+"{}_group.csv".format(group[i])
        rf.response_group(raw=data,path=path)
        print("finish: ", i)


def plot_data(group=[0,2,5,10,15,20,30,40,55,90,100000]):

    plt.figure(figsize=(15,5),dpi=100)
    for i in range(len(group)-1):
        # plt.figure(i)
        plt.xlim(xmin=-20,xmax=520)
        plt.ylim(ymin=0,ymax=1.0)
        data = pd.read_csv(home_path+"{}_group.csv".format(group[i]),header=None)
        data.columns = ['l','R_l']
        plt.plot(data.l,data.R_l,':',linewidth=1,label='{}'.format(group[i]))
        # plt.savefig(home_path+"Q3/group_{}".format(group[i]))
        # plt.close('all')
    plt.legend(loc='upper left',prop={'size':9})
    plt.xlabel("Lag")
    plt.ylabel("Response function bechmarked to prevailing mid quote")
    plt.title("Response fuction(in the unit of bid-ask spread of prevailing quote)")
    plt.show()
    # return data
