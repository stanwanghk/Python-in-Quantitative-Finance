from sklearn.linear_model import LinearRegression
import pandas as pd
from math import log
import numpy as np
import matplotlib.pyplot as plt


home_path = "C:/Users/WPISH/OneDrive/MSc/A_Courses/Spring_Term/MAFS_6010G/homework/Assignment#3/output/"


def slope(data):
    group = [0, 2, 5, 10, 15, 20, 30, 40, 55, 90, 100000]
    ave = size_count(data, group)
    l_range = [10, 20, 30, 40, 50, 75, 100, 125, 150, 175, 200, 250]
    reg = LinearRegression()
    y={}
    for l in l_range:
        y[l]=np.empty(len(group)-1)
    for i in range(len(group) - 1):
        data = pd.read_csv(
            home_path + "{}_group.csv".format(group[i]), header=None)
        data.columns = ['l', 'R_l']
        for l in l_range:
            y[l][i] = (log(data[data.l == l].R_l.values[0]))
    i=1
    for l in l_range:
        plt.figure(i+1)
        plt.plot(ave,y[l],'ob')
        plt.xlabel("log(<V_i>)")
        plt.ylabel("log(R_l|v_i<V<v_i+1)")
        reg.fit(ave.reshape(len(ave),1), y[l])
        y_predict = reg.predict(ave.reshape(len(ave),1))
        plt.plot(ave,y_predict,linewidth=2)
        plt.savefig(home_path+"Q4/l_{}".format(l))
        plt.close('all')
        i +=1
        # print(l, reg.coef_[0])


def size_count(data, group=[0, 2, 5, 10, 15, 20, 30, 40, 55, 90, 100000]):
    ave = np.empty(len(group) - 1)
    for i in range(len(group) - 1):
        group_data = data[(data.Size > group[i]) & (data.Size <= group[i + 1])]
        ave[i] = log(group_data.Size.mean())
        # print(i, group_data.Size.mean())
    return ave
