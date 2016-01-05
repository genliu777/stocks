#!/usr/bin/Rscript

ma<-function(interval, data)
{
  l<-length(data)
#  print("len ");print(l)
  
  ma_data<-NULL
  
  for (i in 1:l) {
    if (i-interval<0) {
      ss<-seq(1, i)
      ma_data<-c(ma_data, sum(data[ss]) / i)
    }
    else {
      ss<-seq(i-interval, i)
      ma_data<-c(ma_data, sum(data[ss]) / interval)
    }
  }
  
  return(ma_data)
}

is_approach<-function(data, delta)
{
  mid<-mean(data)
  flag<-data[((data-mid) / mid) >  delta || (data-mid) / mid < -delta]
  
  if (length(flag) < 1)
      return(TRUE)
  else
    return(FALSE)
}

ma_approach<-function(ma_data, day, delta)
{
#	print(ma_data[c(1,2)])

  ma_5<-ma_data$ma_data_5[ma_data$Date == day]
  ma_10<-ma_data$ma_data_10[ma_data$Date == day]
  ma_20<-ma_data$ma_data_20[ma_data$Date == day]
  ma_30<-ma_data$ma_data_30[ma_data$Date == day]
  ma_60<-ma_data$ma_data_60[ma_data$Date == day]
  ma_120<-ma_data$ma_data_120[ma_data$Date == day]
  ma_180<-ma_data$ma_data_180[ma_data$Date == day]

#	print(c(ma_5, ma_10, ma_20, ma_30, ma_60, ma_120, ma_180))
  
  short <- is_approach(c(ma_5, ma_10, ma_20), delta)
  middle <- is_approach(c(ma_10, ma_30, ma_60), delta)
  long <- is_approach(c(ma_30, ma_120, ma_180), delta)
  return(c(short, middle, long))
}

argv<-commandArgs(TRUE)
file_path<-argv[1]
which_day<-argv[2]

stock<-read.table(file_path, header=TRUE, sep=",")
#stock<-stock[order(stock$date, decreasing=TRUE), ]
close_price<-stock$close

ma_data_5<-ma(5, close_price)
ma_data_10<-ma(10, close_price)
ma_data_20<-ma(20, close_price)
ma_data_30<-ma(30, close_price)
ma_data_60<-ma(60, close_price)
ma_data_120<-ma(120, close_price)
ma_data_180<-ma(180, close_price)

ma_data<-data.frame("Date"=as.Date(stock$date), ma_data_5, ma_data_10, ma_data_20, ma_data_30, ma_data_60, ma_data_120, ma_data_180)

approach_flag<-ma_approach(ma_data, as.Date(which_day), 0.05)

if (approach_flag[1]) {
	print(file_path)
	print(which_day)
	print(approach_flag)
}
