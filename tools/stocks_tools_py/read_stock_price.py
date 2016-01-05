#!/usr/bin/python

import string

#file is cvs
def read_stock_price(stock, header=True):
	price_table = {}
	try:
		file = open(stock, "r")
		lins = file.readlines()
		file.close()
	except:
		return None

	return 	
	

if __name__ == "__main__":
	read_stock_price()
