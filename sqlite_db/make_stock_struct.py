#!/usr/bin/env python
#coding=utf-8
import sqlite3
import os

def make_stock_struct_table(connect, stock_code):
	cursor = connect.cursor()
	#10K unit
	sql = "create table '{0}_stock_struct' (day text, amount float, \
											flow_restrict float, other float, flow float, \
											flow_a float, resaon text)". format(stock_code)
	print sql
	cursor.execute(sql)		

def valid_float(float_str):
	if float_str.replace(".", "").isalnum():
		return float_str
	else:
		return "0"
	
def stock_struct_to_db(file_name, stock_code, connect):
	Day,Amount, Flow_Restrict, Other, Flow, Flow_A, Resaon = range(0, 7)
	f = open(file_name, "r")	
	contents = f.readlines()
	f.close()
	if len(contents) < 1:
		return False

	make_stock_struct_table(connect, stock_code)
	
	for line in contents:
		line = line.strip()
		if line.startswith("单位:万股"):
			days = line.split(" ")
		elif line.startswith("总股本"):
			amount = line.split(" ")
		elif line.startswith("已上市流通A股"):
			flow_a = line.split(" ")

	if not days and len(days) < 1:
		return False

	if not amount and len(amount) < 1:
		return False

	if not flow_a and len(flow_a) < 1:
		return False


#	print table
	l = len(days)
	for i in range(1, l):
		add_stock_struct_sql = "insert into '{0}_stock_struct' values ('{1}', {2}, {3}, {4}, {5}, {6}, '{7}')". \
														format(stock_code, \
														days[i], valid_float(amount[i].replace(",", "")), \
														0, 0, 0, \
														valid_float(flow_a[i].replace(",", "")), "...")
		print add_stock_struct_sql 
		connect.cursor().execute(add_stock_struct_sql)
	return True

	
stock_struct_dir = ""
sqlite_db_path = "ss.db"
save_dir = "../data/stock_struct/eastmoney"

if __name__ == "__main__" :
	conn = sqlite3.connect(sqlite_db_path)
	file_list = os.listdir(save_dir)	
	i = 0 

	for f in file_list:
		if stock_struct_to_db(save_dir+"/"+f, f, conn):
			i += 1
		print i, f

	conn.commit()
	conn.close()

