#!/opt/R/bin/Rscript
args<-commandArgs(TRUE)

finance = read.table(args)
finance
# leverage
#leverage = finance['总负债']/finance['总资产']

# profit
#profit_raito = finance['净利润'] / finance['总资产']




