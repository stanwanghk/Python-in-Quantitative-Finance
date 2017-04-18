#########################################################################################
############  Code for Fama-French Three Factor Model  ###############
#########################################################################################
#  Uses monthly data from Jan-69 to Dec-98

setwd('~/Documents/data/')
# FF_data = read.table("FamaFrench_mon_69_98.txt",header=T)
# attach(FF_data)
# library("Ecdat")
# data(CRSPmon)
# ge = 100*CRSPmon[,1] - RF
# ibm = 100*CRSPmon[,2] - RF
# mobil = 100*CRSPmon[,3] - RF
# stocks=cbind(ge,ibm,mobil)
#########################################
# data is modified by python
# read data
FF_data = read.csv("Asia_Pacific_ex_Japan_6_Factors_Daily.csv",header=T)
attach(FF_data)
daily_price = read.csv("daily price in USD.csv",header=T)
attach(daily_price)
stocks=cbind(HSBC.Holdings,HKEx,ICBC,
               Ping.An,CLP.Holdings,HK...China.Gas,
               China.Res.Power,CKI.Holdings,Wharf.Holdings,
               Henderson.Land,CKH.Holdings,Swire.Pacific.A)
# regression
fit <- lm(cbind(HSBC.Holdings,HKEx,ICBC,
               Ping.An,CLP.Holdings,HK...China.Gas,
               China.Res.Power,CKI.Holdings,Wharf.Holdings,
               Henderson.Land,CKH.Holdings,Swire.Pacific.A)~Mkt.RF+SMB+HML+RMW+CMA+WML)
options(digits=3)
fit
company_name <- list("HSBC.Holdings","HKEx","ICBC",
               "Ping.An","CLP.Holdings","HK...China.Gas",
               "China.Res.Power","CKI.Holdings","Wharf.Holdings",
               "Henderson.Land","CKH.Holdings","Swire.Pacific.A")
adj_r_square <- 0
for (i in 1:12){
    adj_r_square[i] <- summary(fit)[[i]]$adj.r.squared
}
cbind(company_name,adj_r_square)
# significant test
summary(fit)[[1]]
summary(fit)[[2]]
# covariance matrix
cor(cbind(Mkt.RF,SMB,HML,RMW,CMA,WML))
cor(fit$residuals[,1:5])
cor.test(fit$residuals[,1], fit$residuals[,2])
# cor.test(fit$residuals[,1], fit$residuals[,3])
# cor.test(fit$residuals[,2], fit$residuals[,3])
pairs(fit$residuals, lower.panel = NULL)

## Estimation of covariance matrix based on Fama-French three factor model

sigF = as.matrix(var(cbind(Mkt.RF,SMB,HML,RMW,CMA,WML)))
bbeta = as.matrix(fit$coef[,1:5])
bbeta = t( bbeta[-1,])
n=dim(stocks)[1]
sigeps = (n-1)/(n-7) * as.matrix((var(as.matrix(fit$resid[,1:5]))))
sigeps = diag(as.matrix(sigeps))
sigeps = diag(sigeps,nrow=5)
cov_equities = bbeta %*% sigF %*% t(bbeta) + sigeps

options(digits=5)
sigF
bbeta
sigeps
bbeta %*% sigF %*% t(bbeta)
cov_equities
cov(stocks[,1:5])

