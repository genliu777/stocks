#!/usr/bin/python
# coding=gbk

import time
import codecs
import socket
import os
import pycurl
import cStringIO
import sys
import re
import string
import json
from xml.dom.minidom import parse, parseString

sys.path.append("../../../tools/stocks_tools_py/")
from read_stock_list import read_stock

def change_dir(dir):
	try:
		os.mkdir(dir)
	except OSError:
		pass
	finally:
		os.chdir(dir)


def wget(url, file):	
	try :
		buf = cStringIO.StringIO()

		c = pycurl.Curl()
		c.setopt(c.URL, url)
		c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0")
		c.setopt(c.WRITEFUNCTION, buf.write)
		c.perform()

		f = open(file, "w")
		f.write(buf.getvalue())
	finally:
		pass

def wget2(url):
	try:
		buf = cStringIO.StringIO()

		c = pycurl.Curl()
		c.setopt(c.URL, url)
		c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0")
		c.setopt(c.WRITEFUNCTION, buf.write)
		c.perform()

		s = buf.getvalue()
		buf.close()
		return s
	finally:
		pass

	return None
	
if __name__ == "__main__":
	stocks = read_stock("sz")
	i=0
	for k,v in stocks.items()[700:]:
		print i, v[0], v[1]
		url = "http://xueqiu.com/S/SZ{0}/historical.csv".format(v[0])
#		url = "http://real-chart.finance.yahoo.com/table.csv?s={0}.SS&ignore=.csv".format(v[0])
		wget(url, "../../../data/price/sz/xueqiu/{0}".format(v[0]))
		i += 1
