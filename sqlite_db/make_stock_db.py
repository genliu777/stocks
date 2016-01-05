#!/usr/bin/env python

import os
import string
import sqlite3
import sys
sys.path.append("../tools/stocks_tools_py/")
from read_stock_list import *

def import_xueqiu_quote(file_path, connect):
	cursor = connect.cursor()

	files = os.listdir(file_path)
	for file in files:
		full_file_path = file_path + '/' + file
		f = open(full_file_path)
		lines = f.readlines()
		f.close()

		make_table_sql = "create table '{0}' (date text, open float, high float, low float, close float, volume int)".format(file)
		cursor.execute(make_table_sql)

		#symbol,date,open,high,low,close,volume
		head = lines[0]

		#delete header
		for line in lines[1:]:
			item = line.split(",")
			add_quote_sql = "insert into '{0}' values ('{1}', {2}, {3}, {4}, {5}, {6})".format(file, item[1], item[2], item[3], item[4], item[5], item[6])
			cursor.execute(add_quote_sql)


def make_quote_table(connect):
	xueqiu_sh_dir="e:/gww/MIT/stock/data/price/sh/xueqiu"
	xueqiu_sz_dir="e:/gww/MIT/stock/data/price/sz/xueqiu"

	import_xueqiu_quote(xueqiu_sh_dir, connect)
	import_xueqiu_quote(xueqiu_sz_dir, connect)


def make_stocks_list_table(connect):
	cursor = connect.cursor()
	cursor.execute("create table 'stocks' (id int, code text, name text, market int, IPO text, delisting text, web text)")

	sh_list = read_stock("sh")
	sz_list = read_stock("sz")

	i=1

	for code,name,shorthand in sh_list.values():
		sql = "insert into 'stocks' values ({0}, '{1}', '{2}', 1, '', '', '')".format(i, code, name)
	#	print(sql)
		cursor.execute(sql)
		i += 1

	for code,name in sz_list.values():
		cursor.execute("insert into 'stocks' values ({0}, '{1}', '{2}', 2, '', '', '')".format(i, code, name))
		i += 1

	return i

def make_market_table(connect):
	cursor = connect.cursor()

	cursor.execute("create table 'market' (id int, name text, web text)")
	cursor.execute("insert into 'market' values (1, 'sh', '')")
	cursor.execute("insert into 'market' values (2, 'sz', '')")

def make_stock_db(connect):
	make_market_table(connect)
	make_stocks_list_table(connect)
	make_quote_table(connect)

	
if __name__ == "__main__":
	conn = sqlite3.connect("../data/stock_db/stocks.db")	
	make_stock_db(conn)
	conn.commit()
	conn.close()
