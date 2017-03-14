import matplotlib.pyplot as plt
import numpy as np
from math import log

a=0.02
b=0.001
dt=0.25
T=30

def spot_curve():
    spotCurve=np.zeros(121)
    for i in range(len(spotCurve)):
        spotCurve[i] = a+b*(i/4)
    return spotCurve

def discount_curve():
    spotCurve=spot_curve()
    discountCurve = np.zeros(121)
    for i in range(121):
        discountCurve[i]=1/(1+spotCurve[i]*dt)**(i)
    return discountCurve

def forward_curve():
    forwardCurve=np.zeros(120)
    discount=discount_curve()
    for i in range(120):
        #forwardCurve[i]=4*log(1+(a+b*dt)*dt)+i*(b*dt)/(1+(a+b*dt)*dt)
        forwardCurve[i]=4*(discount[i]/discount[i+1]-1)
    return forwardCurve

def swap_curve():
    swapCurve=np.zeros(61)
    discountCurve=discount_curve()
    swapCurve[0]=float('inf')
    for i in range(1,61):
        sum = 0
        for j in range(1,i+1):
            sum += 0.5*discountCurve[j*2]
        #print(i,"  ",sum)
        swapCurve[i]=(1-discountCurve[i*2])/sum
        #print(swapCurve[i])
    return swapCurve

toplot=swap_curve()
name="swap"
term=np.zeros(61)
for i in range(61):
    term[i]=i/2
plt.plot(term,toplot)
plt.xlabel("Term")
plt.ylabel("{} Rate".format(name))
plt.title("The {} curve".format(name))
plt.show()
