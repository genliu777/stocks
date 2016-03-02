#!/usr/bin/Rscript

seq.txt<-"adjust_after_limit_up.txt"
seq.data<-read.table(seq.txt)
seq.data<-seq.data[seq.data[[1]] < 0.11 & seq.data[[1]] > -0.11 , ]
breaks<-seq.data(-0.1, 0.1, 0.01)
hist(seq.data, breaks=200, probability = TRUE)

limit_up<-seq.data[seq.data > 0.09]
limit_down<-seq.data[seq.data < -0.09]
