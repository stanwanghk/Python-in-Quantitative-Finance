"""
Created on Sun Nov  6 16:26:56 2016

@author: Stan Wang

Assignment_1 Delta hedging of an option
"""
import scipy as sp
import math
import numpy as np
import scipy.stats as ss

def d1(S0, K, r, sigma, T):
    return (np.log(S0/K) + (r + sigma**2 / 2) * T)/(sigma * np.sqrt(T))

def d2(S0, K, r, sigma, T):
    return (np.log(S0/K) + (r - sigma**2 / 2) * T)/(sigma * np.sqrt(T))

# the Black-Shoes option price
def BS_Call(S0, K, r, sigma, T):
    return S0 * ss.norm.cdf(d1(S0, K, r, sigma, T)) - K * np.exp(-r * T) * ss.norm.cdf(d2(S0, K, r, sigma, T))

def MC_deltaHedging_Call(S               # stock  price
                        ,X               # strike price
                        ,T               # maturity
                        ,sigma           # volatility
                        ,expectedReturn  # the stock's expected Return
                        ,r               # riskless return rate
                        ,numMC           # number of Monte Carlo
                        ,numsim          # number of days to the maturity
                        ):
    dt = T/float(numsim)
    drift=(r-0.5*sigma*sigma)*dt
    sigmasqrtdt = sigma * math.sqrt(dt)
    portfolio = sp.zeros([numMC],dtype=float)
    interest = np.exp(r*dt)
    # Assume that we adjust our portfolio at the beginning of the business day;
    for j in range(0,numMC):
        # At the first day
        #print("In the first day: ")
        stockPrice = S
        callValue01 = BS_Call(stockPrice,X,r,sigma,T)
        # according to BS, delta=N(d1)
        delta01 = ss.norm.cdf(d1(stockPrice,X,r,sigma,T))
        # we long one call option, and short delta stock to hedge it.
        # and we put the extra money(positive or negative)
        # into the money account
        moneyAccount =  delta01 * stockPrice - callValue01
        print("the stock price is {}".format(stockPrice))
        print("to hedge one call option, we sell {} shares of stock".format(delta01))
        # From  the second day to the last day
        for i in range(1,numsim):
            print("in the {} day: ".format(i+1))
            # assume that the stock price is GBM
            e = sp.random.normal(0,1)
            stockPrice *= np.exp(drift + sigmasqrtdt * e)
            print("the stock price is {}".format(stockPrice) )
            # every day the money in the money account will earn or pay
            # interest at the rate of r;
            moneyAccount *= interest
            # the call value and corresponding delta;
            callValue02 = BS_Call(stockPrice,X,r,sigma,T-i*dt)
            delta02 = ss.norm.cdf(d1(stockPrice,X,r,sigma,T-i*dt))
            # P&L of this call option;
            PnL_call = callValue02 - callValue01
            print("the P&L of the option is {}".format(PnL_call))
            print("the new delta is {}".format(delta01))
            # due to new delta, we need to buy or sell stocks at the value of
            # delta01 - delta02 which means buying if positive, or selling if
            # negative;
            print("the amount of stock we changed is {}".format(delta01-delta02))
            # adjust the value of money account;
            moneyAccount +=(delta02-delta01)*stockPrice
            delta01 = delta02
            callValue01=callValue02
        # At maturity, the call value is given by terminal condition;
        e = sp.random.normal(0,1);
        stockPrice *= math.exp(drift+sigmasqrtdt * e)
        print("the stock price at maturity is {}".format(stockPrice))
        callValue = max(stockPrice-X,0)
        print("the call value at maturity is {}".format(callValue))
        # we can caculated the portfolio value at maturity;
        moneyAccount *= interest
        portfolio[j] = moneyAccount+callValue-delta01*stockPrice
        print("the portfolio at maturity is {}".format(portfolio[j]))
    # After numMC of Monte Cal
    portfolioValue =sp.mean(portfolio)
    return portfolioValue

print("the result from Monte Carlo for delta hedging strategy is {}"
      .format(MC_deltaHedging_Call(100,100,1,0.1,0.1,0.05,100,360)))
