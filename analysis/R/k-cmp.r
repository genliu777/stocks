#!/usr/bin/Rscript
#compare K mmd5 mmd10 mmd20 with the market

argv<-commandArgs(TRUE)

this_stock <- read.table("601872.txt", header=F)
market <- read.table("999999.txt", header=F)

l_this <- length(this_stock[[3]])
l_market <- length(market[[3]])

ll_this_stock<-(this_stock[[3]])[l_this-l_market+1:l_this]

data<-data.frame(ll_this_stock, market[[3]])

s="person cor"
s
cor(ll_this_stock, market[[3]])
cor.test(ll_this_stock, market[[3]])


s="spearman"
s
cor(ll_this_stock, market[[3]], method="spearman")
cor.test(ll_this_stock, market[[3]], metho="spearman")
