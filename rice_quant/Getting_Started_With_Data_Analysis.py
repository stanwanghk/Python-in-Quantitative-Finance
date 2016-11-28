import pandas as pd

# import the module for statistical inference
from scipy import stats as ss

# import the module for plotting
import matplotlib.pyplot as plt
import matplotlib

# import seaborn library
import seaborn as sns

# import the numpy library
import numpy as np

###importing the data

#df1 = pd.read_csv('/Users/WPISH/documents/data.csv')
data_url = "https://raw.githubusercontent.com/alstat/Analysis-with-Programming/master/2014/Python/Numerical-Descriptions-of-the-Data/data.csv"
df = pd.read_csv(data_url)

###Data Transformation
print(df.head()) # the number of rows for head of the data by default is 5
print(df.tail())
print(df.columns) # extracting column names
print(df.index)   # extracting row names or the index
print(df.T)       # transpose data
print(df.sort)    #
print(df.ix[:,0].head()) # extracting a specific column
print(df.ix[10:20,0:3])
print(df.drop(df.columns[[1,2]], axis = 1).head())
 #axis tells the function to drop with respect to columns,if axis=0, then the index

 #Descriptive Statistics
print(df.describe())

 #Hypothesis testing
 #perform one sample t-test using 1500 as the true mean
print(ss.ttest_1samp(a=df.ix[:,'Abra'],popmean=1500))

#Visulization
matplotlib.rcdefaults()

plt.show(df.plot(kind = 'box'))

pd.options.display.mpl_style = 'default' # Sets the plotting display theme to ggplot2
df.plot(kind = 'box')

sns.boxplot(data=df,width=0.5)
sns.violinplot(df,width=3.5)

plt.show(sns.distplot(df.ix[:,2], rug = True, bins = 15))

with sns.axes_style("white"):
    plt.show(sns.jointplot(df.ix[:,1],df.ix[:,2], kind = "kde"))

plt.show(sns.lmplot("Benguet","Ifugao",df))

#Creating custom function
def add_2int(x,y):
    return x+y
print(add_2int(2,2))

# an algorithm example
def case(n=10,mu=3,sigma=np.sqrt(5),p=0.025,rep=100):
    m=np.zeros((rep,4))

    for i in range(rep):
        norm = np.random.normal(loc = mu, scale = sigma, size = n)
        xbar = np.mean(norm)
        low = xbar - ss.norm.ppf(q = 1 - p) * (sigma / np.sqrt(n))
        up = xbar + ss.norm.ppf(q = 1 - p) *(sigma / np.sqrt(n))

        if (mu > low) & (mu < up):
            rem = 1
        else:
            rem = 0

        m[i,:] = [xbar, low, up, rem]

    inside = np.sum(m[:,3])
    per = inside/rep
    desc = "There are {0} confidence intervals that contain \"the true mean \" ({1}), that is {2} percent of total CIs".format(inside, mu, per)

    return {"Matrix": m, "Decision": desc}

# improving the above code
def case2(n=10,mu=3,sigma=np.sqrt(5),p=0.025,rep=100):
    scaled_crit = ss.norm.ppf(q=1-p)*(sigma/np.sqrt(n))
    norm = np.random.normal(loc = mu, scale = sigma, size = (rep,n))

    xbar = norm.mean(1)
    low = xbar - scaled_crit
    up = xbar - scaled_crit

    rem = (mu > low) & (mu < up)
    m = np.c_[xbar,low,up,rem]

    inside = np.sum(m[:,3])
    per = inside / rep
    desc = "There are {0} confidence intervals that contain \"the true mean \" ({1}), that is {2} percent of total CIs".format(inside, mu, per)
    return {"Matrix": m, "Decision": desc}
