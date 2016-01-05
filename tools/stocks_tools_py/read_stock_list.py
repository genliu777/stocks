#!/usr/bin/python
import string

def read_stock(src):
	if src == "sh":
		file_path="e:/gww/MIT/stock/data/stocks/sh_A.txt"
	elif src == "sz":
		file_path="e:/gww/MIT/stock/data/stocks/sz.txt"

	stocks = dict()
	try:
		f = open(file_path, "r")
		stocks_list = f.readlines()
		for stock in stocks_list:
			stock_item = string.split(stock, " ")
			stocks[stock_item[0]] = stock_item
	finally:
		pass

	return stocks	

if __name__  == "__main__" :
	stocks = read_stock("sh")	
	for k,v in stocks.items():
		print v	
