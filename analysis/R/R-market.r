#!/usr/bin/Rscript

#stock price graph

market <- read.table("history", header=T)

#market
par(pch=20)
par(pin=c(6, 2))
par(las=2)
par(xaxs='r')
par(cex.axis=0.5)
par(lty=3)
par(ann=F)

l <- length(market$date)

x=1:l
s<-subset(x, x%%7==1)

market$date<-factor(market$date, order=T)

plot(market$close[l:1], type="b", xaxt='n')

l1 = length(s)
axis(1, at=s, labels=(market$date[s])[l1:1], las=2)

abline(v=c(0.25*l, 0.5*l, 0.75*l), untf=FALSE)
title(main="stock-600010", xlab="date", ylab="price(yuan)")
