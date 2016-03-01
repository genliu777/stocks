#!/usr/bin/env python

import sqlite3
import logging

def calculate_quote_delta(close_price, interval):
	delta_list = []
	for i in range(len(close_price)-1, 0, -1):
		data = close_price[i]
		day = data[0]
		price = data[1]

		try:
			old_price = close_price[i-interval][1]
		except:
			old_price = price	

		delta = (day, price/old_price - 1)
		delta_list.append(delta)
	print delta_list

def stocks_list(connect, market):
	cursor = connect.cursor()
	if market == "sh":
		sql = "select code from 'stocks' where market = 1"	
	elif market == "sz":
		sql = "select code from 'stocks' where market = 2"	
	cursor.execute(sql)
	return cursor.fetchall()

def delta_info(connect, code):
	cursor = connect.cursor()
	
	sql = "select date, close from '{0}'".format(code)

	cursor.execute(sql)
	ret = cursor.fetchall()
	delta_1 = calculate_quote_delta(ret, 1)
	print delta_1	
	pass

if __name__ == "__main__":
	conn = sqlite3.connect("../data/stock_db/stocks.db")
	stocks = stocks_list(conn, "sh")
	delta_info(conn, stocks[0][0])
#	print(stocks)
	conn.commit()
	conn.close()
