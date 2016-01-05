#!/usr/bin/Rscript

#计算移动平均线, 找出黏合的票

argv<-commandArgs(TRUE)

#if (length(argv) < 2) {
#	s = "R-ma.r stock_code"
#	s
#	q()
#}
#

ma<-function(array, interval)
{
	l<-length(array)
	if (l<interval) {
		
	}
}

#read stock file
stock <- read.table("history", header=TRUE)
price<-stock["close"][,1]
length(price)
ma60<-ma(price, 60)
ma10<-ma(price, 10)
ma5<-ma(price, 5)


q()
