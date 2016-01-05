#!/usr/bin/Rscript

pant.result.txt<-"e:/gww/MIT/stock/bin/pant.result"
pant.result<-read.table(pant.result.txt)
pant.result<-pant.result[pant.result[[1]] < 0.11 & pant.result[[1]] > -0.11 , ]
breaks<-seq(-0.1, 0.1, 0.01)
hist(pant.result, breaks=200, probability = TRUE)

limit_up<-pant.result[pant.result > 0.09]
limit_down<-pant.result[pant.result < -0.09]
