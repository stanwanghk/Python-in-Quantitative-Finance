from sklearn.linear_model import LinearRegression
import pandas as pd
from math import log
import numpy as np


home_path = '/home/stan_wp/Documents/data/output/'


def slope(data):
    group = [0, 2, 5, 10, 15, 20, 30, 40, 55, 90, 100000]
    ave = size_count(data, group)
    l = np.array([10, 20, 30, 40, 50, 75, 100, 125, 150, 175, 200, 250])
    reg = LinearRegression()
    for i in range(len(group) - 1):
        data = pd.read_csv(
            home_path + "{}_group.csv".format(group[i]), header=None)
        data.columns = ['l', 'R_l']
        x = np.empty(12)
        for j in range(len(l)):
            x[j] = (log(data[data.l == l[j]].R_l.values[0]))

        reg.fit(l.reshape(12, 1), x)
        print(i, reg.coef_)


def size_count(data, group=[0, 2, 5, 10, 15, 20, 30, 40, 55, 90, 100000]):
    ave = np.empty(len(group) - 1)
    for i in range(len(group) - 1):
        group_data = data[(data.Size > group[i]) & (data.Size <= group[i + 1])]
        ave[i] = log(group_data.Size.mean())
        print(i, group_data.Size.mean())
    return ave
