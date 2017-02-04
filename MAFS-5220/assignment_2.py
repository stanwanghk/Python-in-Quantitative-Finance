"""
@author: Stan Wang

assignment 2 : binomial tree for American options;
"""
import networkx as nx
from math import *
# build the binomial tree. At each node, the value stands for stock price;
def bgoptiongrid(s,T,r,sigma,n):
    # some useful parameters;
    deltaT = T/n
    u = exp(sigma * sqrt(deltaT))
    d = 1.0/u
    a = exp(r*deltaT)
    p = (a-d)/(u-d)
    # G stands for the binomial tree;
    G = nx.Graph()
    G.add_node((0,0),value=s,time=0)
    for i in range(0,n+1):
        for j in range(0,i+1):
            if i<n:
                currentvalue = G.node[(i,j)]['value']
                G.add_node((i+1,j),value = currentvalue*d, time = (i+1)*deltaT)
                G.add_node((i+1,j+1), value = currentvalue*u, time = (i+1)*deltaT)
                G.add_edge((i,j),(i+1,j),value = 1.0 - p)
                G.add_edge((i,j),(i+1,j+1), value = p)
    return G

class SimpleCall:
    def __init__(self,strike,maturity):
        self.strike = strike
        self.maturity = maturity
    def payoff(self,price):
        return max(price - self.strike, 0)

class SimplePut(SimpleCall):
    def payoff(self,price):
        return max(self.strike - price, 0)

def SetEuropeanPayoff(G,n,derivative):
    for i in range(0,n+1):
        G.node[(n,i)]['option'] = derivative.payoff(G.node[(n,i)]['value'])

def EuropeanBackwardInduction(G,n,discount):
    for i in range(n-1,-1,-1):
        for j in range(0,i+1):
            nextdown= G.node[(i+1,j)]['option']
            nextup =G.node[(i+1,j+1)]['option']
            nextdownprob = G[(i,j)][(i+1,j)]['value']
            nextupprob = G[(i,j)][(i+1,j+1)]['value']
            undis = nextup * nextupprob + nextdown * nextdownprob
            G.node[(i,j)]['option'] = discount * undis
    return G.node[(0,0)]['option']

def AmericanBackwardInduction(G,n,discount):
    for i in range(n-1,-1,-1):
        for j in range(0,i+1):
            nextdown= G.node[(i+1,j)]['option']
            nextup =G.node[(i+1,j+1)]['option']
            nextdownprob = G[(i,j)][(i+1,j)]['value']
            nextupprob = G[(i,j)][(i+1,j+1)]['value']
            undis = nextup * nextupprob + nextdown * nextdownprob
            G.node[(i,j)]['option'] = max(discount * undis,derivative.payoff(G.node[(i,j)]['value']))
    return G.node[(0,0)]['option']


s = 100
sigma = 0.1
strike = 100
T = 1
r = 0.05
n = 5
stepdiscount = exp(-r * T/n)
derivative = SimpleCall(strike,T)
# derivative = SimplePut(strike,T)
G = bgoptiongrid(s,T,r,sigma,n)
SetEuropeanPayoff(G,n,derivative)
price_euro = EuropeanBackwardInduction(G,n,stepdiscount)
price_amer = AmericanBackwardInduction(G,n,stepdiscount)
print (price_euro)
print (price_amer)

#Remark: for call options, the European type and the American type have the same price if the underlying asset does not pay enough dividends; but for the put value, the American type is more valueable than the European type.

# another way to code
def binomialcall(s,x,T,r,sigma,n,
                e_a # 0 means European,1 means Ameican;
                ):
    deltaT = T/n
    u = exp(sigma * sqrt(deltaT))
    d = 1.0/u
    a = exp(r*deltaT)
    p = (a-d)/(u-d)
    v = [[0 for j in range(i+1)] for i in range(n+1)]
    for j in range(0,n+1):
        v[n][j] = max(s * u **j * d ** (n-j) - x,0.0)
    for i in range(n-1,-1,-1):
        for j in range(0,i+1):
            v[i][j] = max(exp(- r * deltaT) * (p * v[i+1][j+1] + (1.0 - p) * v[i+1][j]), e_a*max(s*u**j*d**(i-j)-x,0.0))
    return v[0][0]
def binomialput(s,x,T,r,sigma,n,
                e_a # 0 means European,1 means Ameican;
                ):
    deltaT = T/n
    u = exp(sigma * sqrt(deltaT))
    d = 1.0/u
    a = exp(r*deltaT)
    p = (a-d)/(u-d)
    v = [[0 for j in range(i+1)] for i in range(n+1)]
    for j in range(0,n+1):
        v[n][j] = max(x - s * u **j * d ** (n-j),0.0)
    for i in range(n-1,-1,-1):
        for j in range(0,i+1):
            v[i][j] = max(exp(- r * deltaT) * (p * v[i+1][j+1] + (1.0 - p) * v[i+1][j]), e_a*max(x - s*u**j*d**(i-j),0.0))
    return v[0][0]
e_a = 1
print (binomialput(s,strike,T,r,sigma,n,e_a))
print (binomialcall(s,strike,T,r,sigma,n,e_a))
