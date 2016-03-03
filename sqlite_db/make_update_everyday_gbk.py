#!/usr/bin/env python
#coding=gbk

import sqlite3
import string

def moving_average_calculate(price, exist_quote, exist_extra_quote, interval):
	l = len(quote)

	get_pre_price = lambda x,y:x[y][4]
	if interval == 5:
		get_pre_ma = lambda x,y:x[y][0]
	elif interval == 10:
		get_pre_ma = lambda x,y:x[y][1]
	elif interval == 20:
		get_pre_ma = lambda x,y:x[y][2]
	elif interval == 30:
		get_pre_ma = lambda x,y:x[y][3]
	elif interval == 60:
		get_pre_ma = lambda x,y:x[y][4]


	if l - interval < 0:
		summay = get_pre_ma(exist_extra_quote, -1) * l
		my_ma = (summay + price) / (l+1)
	else:
		pre_price = get_pre_price(quote, -interval)
		pre_ma = get_pre_ma(exist_extra_quote, -1)
		my_ma = pre_ma + (price-pre_price)/interval
	return my_ma

def update_moving_average(conn, stock_code, quote, day):
	cursor = conn.cursor()
	exist_quote_sql = "select * from '{0}'".format(stock_code)
	exist_extra_quote_sql = "select * from '{0}_extra'".format(stock_code)

	cursor.execute(exist_quote_sql)
	exist_quote = cursor.fetchall()

	cursor.execute(exist_extra_quote_sql)
	exist_extra_quote = cursor.fetchall()
	
	close_price = quote[4]
	ma5 = moving_average_calculate(close_price, exit_quote, exit_extra_qutoe, 5)
	ma10 = moving_average_calculate(close_price, exit_quote, exit_extra_qutoe,10)
	ma20 = moving_average_calculate(close_price, exit_quote, exit_extra_qutoe,20)
	ma30 = moving_average_calculate(close_price, exit_quote, exit_extra_qutoe,30)
	ma60 = moving_average_calculate(close_price, exit_quote, exit_extra_qutoe,60)

	update_sql = "update '{0}_extra' ma5={1}, \
									ma10={2}, ma20={3}, \
									ma30={4}, ma60={5} \
									where day={6}".format(stock_code, ma5, ma10, ma20, ma30, ma60, day)
	print update_sql
	

def rise_ratio_calculate(price, exist_quote, interval):
	l = len(exist_quote)
	
	if (l-interval) < 0	:
		return 0;
	else:
		pre_close_price = exist_quote[-interval][4]
		return float(price) / float(pre_close_price) - 1	

def update_rise_ratio(conn, stock_code, quote, day):
	cursor = conn.cursor()
	exist_quote_sql = "select * from '{0}'".format(stock_code)

	cursor.execute(exist_quote_sql)
	exist_quote = cursor.fetchall()
	
	close_price = quote[4]
	d1 = rise_ratio_calculate(close_price, exist_quote, 1)
	d5 = rise_ratio_calculate(close_price, exist_quote, 5)
	d10 = rise_ratio_calculate(close_price, exist_quote, 10)
	d20 = rise_ratio_calculate(close_price, exist_quote, 20)
	d30 = rise_ratio_calculate(close_price, exist_quote, 30)
	d60 = rise_ratio_calculate(close_price, exist_quote, 60)

	update_sql = "update '{0}_extra' rratio1={1}, \
									rratio5={2}, rratio10={3}, \
									rratio30={4}, rratio60={5} \
									where day={6}".format(stock_code, d1, d5, d10, d20, d30, day)
	print update_sql


def update_quote(conn, stock_code, quote, day):
	cursor = conn.cursor()
	insert_sql = "insert into '{0}' values ('{1}', {2}, {3}, {4}, {5}, {6})" \
								.format(stock_code, day, quote[1], quote[2], quote[3], quote[4], quote[5])

	insert_extral_sql = "insert into '{0}_extra' values ('{1}', 0,0,0,0,0,0,0,0,0,0,0,{2})" \
								.format(stock_code, day, quote[6])

	print insert_sql
	print insert_extral_sql
	pass
	

def update(conn, day, file_path):
	Stock_code,Open,High,Low,Close,Volume, Volume_ratio,Industry = (0,11,12,13,3,7,10,18)
	f = open(file_path, "r")
	contents = f.readlines()
	f.close()
#	print contents

	for line in contents[1:]:
		row = line.strip().split("\t")
		my_quote =  (row[Stock_code].strip(), row[Open].strip(), \
					row[High].strip(), row[Low].strip(), \
					row[Close].strip(), row[Volume_ratio].strip(), \
					row[Volume].strip(), row[Industry].strip())

		update_quote(conn, row[Stock_code].strip(), my_quote, day)
	#	update_moving_average(conn, row[Stock_code].strip(), my_quote, day)
		update_rise_ratio(conn, row[Stock_code].strip(), my_quote, day)
		break
	

dir_path = "/cygdrive/e/new_zx_allin1/T0002/export/"
if __name__ == "__main__":
	import os
	files = os.listdir(dir_path)	
	day_file = filter(lambda x:x.find("沪深Ａ股")==0 and x.find(".txt")!=-1 , files)

	day = day_file[1][8:16]
	day = "{0}-{1}-{2}".format(day[0:4], day[4:6], day[6:8])
	print day_file, day

	conn = sqlite3.connect("stocks.db")	
	update(conn, day, dir_path+"/"+day_file[1])
#	print day_file

