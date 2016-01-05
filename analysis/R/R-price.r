#!/opt/R/bin/Rscript

#price is at bottom

#arg1=start time
#arg2=stock_code

argv<-commandArgs(TRUE)

if (length(argv) < 2) {
	s = "R-price.r start_time stock_code"
	s
	q(1)
}

start_time<-argv[1]
stock_code<-argv[2]

#stock_file<-stock_code+"/market_history.csv"
market<-read.table("history", header=T)


