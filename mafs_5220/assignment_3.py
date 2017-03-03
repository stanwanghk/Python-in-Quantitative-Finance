"""
author: Stan Wang;
assignment 3 : trinomial tree for option pricing;

"""
import networkx as nx
import numpy as np

def tri_option_grid(S,dt,u,d,pu,pd,pm,numsim):
    G = nx.Graph()
    G.add_node((0,0),value=S,time=0)
    for i in range(0,numsim):
        for j in range(0,2*i+1):
            currentvalue = G.node[(i,j)]['value']
            G.add_node((i+1,j),value=currentvalue*u,time=(i+1)*dt)
            G.add_node((i+1,j+1),value=currentvalue,time=(i+1)*dt)
            G.add_node((i+1,j+2),value=currentvalue*d,time=(i+1)*dt)
            G.add_edge((i,j),(i+1,j),value = pu)
            G.add_edge((i,j),(i+1,j+1),value = 1-pu-pd)
            G.add_edge((i,j),(i+1,j+2),value = pd)
    return G
# the class for simple call and put
class simpleCall:
    def __init__(self,strike,maturity):
        self.strike = strike
        self.maturity = maturity
    def payoff(self,price):
        return max(price - self.strike, 0)
class simplePut:
    def __init__(self,strike,maturity):
        self.strike = strike
        self.maturity = maturity
    def payoff(self,price):
        return max(self.strike - price, 0)
def option(strike,maturity,c_p):
    if c_p==0:
        return simpleCall(strike,maturity)
    else:
        return simplePut(strike,maturity)
# set the terminal payoff for option
def set_terminal_payoff(G,n,derivative):
    for i in range(0,2*n+1):
        G.node[(n,i)]['option'] = derivative.payoff(G.node[(n,i)]['value'])
#backward
def backward_induction(G,n,discount,derivative,e_a):
    for i in range(n-1,-1,-1):
        for j in range(0,2*i+1):
            nextup = G.node[(i+1,j)]['option']
            nextm = G.node[(i+1,j+1)]['option']
            nextdown = G.node[(i+1,j+2)]['option']
            nextupprob = G[(i,j)][(i+1,j)]['value']
            nextmprob =G[(i,j)][(i+1,j+1)]['value']
            nextdownprob =G[(i,j)][(i+1,j+2)]['value']
            undis = nextup*nextupprob+nextm*nextmprob+nextdown*nextdownprob
            G.node[(i,j)]['option'] = max(undis * discount,e_a*derivative.payoff(G.node[i,j]['value']))
    return G.node[(0,0)]['option']

def tri_option_price(S        # stock price
                     ,K       # strike price
                     ,T       # maturity
                     ,numsim  # number of simulations
                     ,sigma   # vol
                     ,r       # riskless rate
                     ,e_a     # 0 means European option, 1 means Amercian option
                     ,c_p     # 0 means Call option, 1 means Put option
                     ):
    dt = T/float(numsim)
    u  = np.exp(sigma * np.sqrt(2*dt))
    d  = 1/u
    numerator = np.exp(sigma*np.sqrt(dt/2))-np.exp(-sigma*np.sqrt(dt/2))
    pu = ((np.exp(r*dt/2)-np.exp(-sigma*np.sqrt(dt/2)))/numerator)**2
    pd = ((np.exp(sigma*np.sqrt(dt/2))-np.exp(r*dt/2))/numerator)**2
    pm = 1-pu-pd
    stepdiscount = np.exp(-r * dt)
    derivative = option(K,T,c_p)
    G  = tri_option_grid(S,dt,u,d,pu,pd,pm,numsim)
    set_terminal_payoff(G,numsim,derivative)
    option_price = backward_induction(G,numsim,stepdiscount,derivative,e_a)
    return option_price

print(tri_option_price(100,100,1,255,0.1,0.05,0,0))