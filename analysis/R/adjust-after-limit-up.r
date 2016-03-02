#!/usr/bin/Rscript

argv <- commandArgs(TRUE)
file_path<-argv[1]
which_day<-argv[2]
#which_day<-"2015-08-01"
print(file_path)
#print(which_day)

stock<-read.table(file_path, header=TRUE, sep=",")
yes_close_price<-c(stock$open[1], stock$close[1:length(stock$close)-1])
stock$yes_close<-yes_close_price

stock<-stock[order(stock$date, decreasing=FALSE), ]

stock<-stock[as.Date(stock$date) > as.Date(which_day), ]
stock<-stock[(stock$close != 0.0),  ]

len<-length(stock[[1]])
if ( len < 60) {
#	print(len)
	stop("data is too less")
}

stock<-within(stock, {
	price_delta<-close/yes_close -1 
})

adjust_after_limit_up_seq<-function(price_delta) {
	l<-length(price_delta)
	ll<-1:l
	limit_up<-ll[price_delta > 0.095]
  if (length(limit_up)<3)
    return()
	
	limit_up<-price_delta > 0.095
	next_day_delta<-c((price_delta < 0.03 & price_delta > -0.03)[-1], FALSE)
	
	limit_up_with_pant <- ll[limit_up & next_day_delta ]

	lu<-length(limit_up_with_pant)
	
	if (lu < 1)
	  return()

	limit_up_with_pant_seq<-array(c(limit_up_with_pant, limit_up_with_pant+1, limit_up_with_pant+2), dim=c(lu, 3))

	for (i in 1:lu)	 {
		item<-price_delta[limit_up_with_pant_seq[i, ]	]
		print(item)
	}		
}

adjust_after_limit_up_seq(stock$price_delta)->x
