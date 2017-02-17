from scipy.optimize import root
from math import pow

def diff(x):
    return marketPrice-(1+(c/x-1)*(1-pow((1+x*dt),-(T/dt))))

T  = 1            #time to maturity
dt = 0.5          #the step time
marketPrice = 1   #current market price
c  = 0.01         #coupon rate


sol = root(diff,0.2)
print(sol.x)
