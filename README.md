# Python in Quantitative Finance
as a student majoring in Financial Mathematics, i think that python is a very useful tool to quantitative research. so i create this project to record and share what i have learned in the course and by myself.

*******

## Volatility Forecast in SSE&SHE with Machine Learning and Sentimental Analysis(newsVF)
There is a huge need for effective forecasting of financial risk, which is usually implied by the related volatility. Hence the concept of financial volatility, a required parameter for pricing many kinds of financial assets and derivatives (i.e. options), is critical. I now pursue a reasonable mathematical model to achieve efficient prediction of financial volatility. And I realized that online information can have a substantial effect on the trading price or trading volume of a stock or index. In summary, I will forecast volatility, relying partly on the sentiment analysis of online information, using a GARCH-based SVM approach.The basic architecture of this approach is in Figure 0.1. 
![Alt text](https://github.com/stanwanghk/Python-in-Quantitative-Finance/blob/master/newsVF/flowchart.png)

### stage 1 financial news and stock crawling

using a crawler to collect news of a given company for a given period, and storing them in a SQLite DB(not uploaded to github);
using TuShare to crawl the stock information.

### stage 2 sentimental analysis

ddl: Apr 1st
### stage 3 volatility forecast based on SVM


********

## HOMEWORK

### MAFS_5220 Quantitative and statistics analysis
In this course, I will do some homework about quantitative in python, and a final project in Machine Learning.

### MAFS_5040 Quantitative methods for fixed-income instruments
There are some codes to calculate the yield, DV01, duration, convexity etc.
