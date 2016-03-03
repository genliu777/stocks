#!/usr/bin/env python

import os
import string
import sqlite3
import sys

zxzq_export_dir = "/cygdrive/e/new_zx_allin1/T0002/export/"

def import_zxzq_quote(file_path, connect, stock_code):
	cursor = connect.cursor()

	f = open(zxzq_export_dir+"/"+file_path)
	lines = f.readlines()
	f.close()

	print zxzq_export_dir+"/"+file_path

	make_table_sql = "create table '{0}' \
										(date text, open float, high float, low float, \
										close float, volume int)".format(stock_code)

	cursor.execute(make_table_sql)

	#symbol,date,open,high,low,close,volume
	head = lines[0]

	#delete header
	for line in lines[2:-1]:
		item = line.strip().split("\t")
		print item
		add_quote_sql = "insert into '{0}' values ('{1}', {2}, {3}, {4}, {5}, {6})". \
												format(stock_code, item[0].replace("/", "-"), 
												item[1], item[2], item[3], item[4], item[5])
		print add_quote_sql
		cursor.execute(add_quote_sql)

def make_quote_table(stocks_file, connect):
	for stock_file in stocks_file:
		import_zxzq_quote(stock_file, connect, stock_file[3:9])

def which_market(stock_code):
	if stock_code.find("SH") != -1 or stock_code.find("sh")!= -1:
		return 1;
	if stock_code.find("SZ") != -1 or stock_code.find("sz") != -1:
		return 2;
	

def make_stocks_list_table(connect):
	cursor = connect.cursor()
	cursor.execute("create table 'stocks' (id int, code text, name text, market int, IPO text, delisting text, web text)")

	stocks = os.listdir(zxzq_export_dir)
	stocks = filter(lambda x:x.find("SH")==0 or x.find("SZ")==0, stocks)

	i=1
	for stock in stocks:
		sql = "insert into 'stocks' values ({0}, '{1}', 'xxxx', {2}, '', '', '')".format(i, stock[3:9], which_market(stock))
		print sql
		cursor.execute(sql)
		i += 1

	return stocks

def make_market_table(connect):
	cursor = connect.cursor()

	cursor.execute("create table 'market' (id int, name text, web text)")
	cursor.execute("insert into 'market' values (1, 'sh', '')")
	cursor.execute("insert into 'market' values (2, 'sz', '')")

def make_stock_db(connect):
	make_market_table(connect)
	stocks_file = make_stocks_list_table(connect)
	make_quote_table(stocks_file, connect)

	
if __name__ == "__main__":
#	conn = sqlite3.connect("../data/stock_db/stocks.db")	
	conn = sqlite3.connect("stocks.db")	
	make_stock_db(conn)
	
	conn.commit()
	conn.close()
