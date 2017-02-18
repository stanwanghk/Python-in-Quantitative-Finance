import matplotlib.pyplot as plt
import numpy as np


def spotRate(a,b):
    spotCurve=np.zeros(121)
    for i in spotCurve:
        spotCurve[i] = a+b*(i/4)
    plt.plot(spotCurve)
    return spotCurve

#def discountCurve()

a=0.02
b=0.001

spotRate(a,b)