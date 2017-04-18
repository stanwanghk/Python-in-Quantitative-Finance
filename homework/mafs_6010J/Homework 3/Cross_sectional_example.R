## Example for cross-sectional factor model 

setwd('~/Documents/data/')
# berndtInvest = read.csv("berndtInvest.csv")
# summary(berndtInvest)
# returns = berndtInvest[,-c(1,11,18)] # exclude the column 1,11,18
# ind_codes = as.factor(c(3,3,2,1,1,2,3,3,1,2,2,3,1,2,3))
# codes = as.matrix(model.matrix(~ind_codes))
# codes[,1] =  1 - codes[,2] - codes[,3]
# betas = as.data.frame(codes)
# colnames(betas) = c("tech","oil","other")
# rownames(betas) = colnames(berndtInvest[,-c(1,11,18)])
# betas

# data process is done by python
# regression
returns = read.csv("stocks_HSI100.csv")
betas = read.csv("sector_HSI100.csv")
n = dim(returns)[1]
factors = matrix(0,nrow=n,ncol=5)
adj_r_squared = matrix(0,nrow=n)
resid = matrix(9,nrow=n,ncol=5)
for (i in 1:n)
{
  return_data = cbind(t(returns[i,-1]),betas)
  return_data = na.omit(return_data)
  lmfit = lm(return_data[,1]~return_data[,2]+return_data[,3]+return_data[,4]+return_data[,5])
  factors[i,]= lmfit$coef
  adj_r_squared[i]=summary(lmfit)$adj.r.squared
  resid[i,]=summary(lmfit)$resid[1:5]
}
plot(adj_r_squared,xlab="month",ylab="adjusted R^2")
# mean and covariance matrix
colnames(factors) = c("overall","Financial","Information technology","Industrial","Real estate")
mean_factor = matrix(0,nrow=1,ncol=5)
for (i in 1 :5){
    mean_factor[1,i] = mean(factors[i])
}
cov(factors)
# ## pdf("berndt_cross_section_factors.pdf",width=7,height=3)
# par(mfrow=c(1,3),cex.axis=1.08,cex.lab=1.08,cex.main=1.05)
# plot(factors[,1],type="b",lty="dotted",
#      lwd=2,xlab="month",ylab="factor",main="market")
# plot(factors[,2],lty="dotted",lwd=2,type="b",
#      xlab="month",ylab="factor",main="technology")
# plot(factors[,3],lty="dotted",lwd=2,type="b",
#      xlab="month",ylab="factor",main="oil")
# ## graphics.off()
# options(digits=2)
# sqrt(diag(cov(factors)))
## pdf("berndt_cross_section_factors_acf.pdf",width=6,height=6)
## acf(factors,ylab="",xlab="lag")
## graphics.off()

## Estimation of covariance matrix based on Fama-French three factor model
sigF = as.matrix(var(factors))
bbeta = as.matrix(cbind(1,betas))[1:5,]
sigeps = (n-1)/(n-5) * as.matrix((var(resid)))
sigeps = diag(as.matrix(sigeps))
sigeps = diag(sigeps,nrow=5)
cov_equities = bbeta %*% sigF %*% t(bbeta) + sigeps

options(digits=5)
sigF
bbeta
sigeps
bbeta %*% sigF %*% t(bbeta)
cov_equities
cov(returns[,2:6])

