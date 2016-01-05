#!/usr/bin/env python
import sys
import urllib

import xls2csv

def wget(url, file):
	return urllib.urlretrieve(url, file)

def write_to_sqlite(lines, connect=None):
	CODE,NAME,CLOSE,DELTA,VOLUME, OPEN,CLOSE_YES,HIGH,LOW	= (0,1,2,3,8,9,10,11,12)
	if (connect == None):
		import sqlite3
		#open stock.sb
		connect = sqlite3.connect("../../../data/stock_db/stocks.db")

	cursor = connect.cursor()

	#line[0] is title
	#line[1] is column title

	day = lines[0].split(",")[1].split(" ")[0]

	import time
	year = time.strftime("%Y", time.gmtime())
	day = year + "-" +day
	

	for line in lines[2:] :
		columns = line.split(",")
		#start with sh or sz
		stock_code = columns[CODE][2:]

		if columns[CODE].find("sh") != -1:
			market = 1
		else:
			market = 2
			continue
		
	#	table desc --> "create table '{0}' 
	# (date text, open float, high float, low float, close float, volume int)"

		sql = "insert into '{0}' values ('{1}', {2}, {3}, {4}, {5}, {6})". \
				format(stock_code, day, columns[OPEN], columns[HIGH], columns[LOW], columns[CLOSE], columns[VOLUME])	

		try:
			print(sql)
			cursor.execute(sql)
		except:
			print(sql+"error\n")

	pass

if __name__ == "__main__":
	url = "http://stock.gtimg.cn/data/get_hs_xls.php?id=ranka&type=1&metric=chr"

	import time
	today=time.strftime("%Y-%m-%d")
	xls_file = today + ".xls"
	wget(url, xls_file)

#	xls_file = "2016-01-04.xls"

	lines = xls2csv.xls2csv_lines(xls_file)
	write_to_sqlite(lines, None)
	
