import matlab.engine as mat
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

eng = mat.start_matlab()


def read_data(date="199712"):
    cov = pd.read_csv("cov_{}.csv".format(date), index_col=1)
    mu = pd.read_csv("mu_{}.csv".format(date), index_col=1)
    return cov, mu


def back_test(start=(1997, 12), end=(2016, 12)):
    hist_return = {}
    key = start
    while key != end:
        # get the data
        cov, mu = read_data(str(key[0]) + str(key[1]))

        # adjust if the stocks pool changes
        if key == start:
            target_return = mu.mean()
            alpha = np.array(eng.initialpos(cov,
                                            mu, target_return)._data)
        else:
            # calculate the return of the last month portfolio
            hist_return.append(np.dot(alpha, mu[:alpha.size]))

        # update the target return
            # strategy 1: target return equals the average return of stocks
            target_return = mu.mean()
            # strategy 2: medien
            target_return = mu.median()

            # solve the mean_variace problem
            alpha_0 = np.append(alpha,np.zeros(mu.size - alpha.size))
            alpha = np.array(eng.portfolio(cov,
                                           mu, alpha_0, target_return)._data)
        # next month
        key[1] += 1
        if key[1] > 12:
            key[0] += 1
            key[1] = 1
    return hist_return


def plot_hist_return(raw):
    plt.plot(range(raw))
