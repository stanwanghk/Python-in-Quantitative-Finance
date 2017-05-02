import response_function as rf
import pandas as pd
import matplotlib.pyplot as plt


home_path = '/home/stan_wp/Documents/data/output/'

def group_load(data,group=[0,2,5,10,15,20,30,40,55,90,100000]):
    for i in range(len(group)-1):
        group_data = data[(data.Size>group[i])&(data.Size<=group[i+1])]
        out = rf.response_fun(group_data)
        file = open(home_path+"{}_group.csv".format(group[i]),'w')
        for j in range(len(out)):
            file.write('{},{}\n'.format(j,out[j]))
        file.close()
        print("finish: ", i)


def plot_data(num):
    data = pd.read_csv(home_path+"{}_group.csv".format(num),header=None)
    data.columns = ['l','R_l']
    plt.plot(data.l,data.R_l,label='{}'.format(num))
    # return data
