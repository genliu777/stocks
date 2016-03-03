#!/usr/bin/python
# coding=utf8

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
	

def save(name, content, dir_path):
	try:
		f = codecs.open(dir_path+"/"+name, "w", "utf-8")
		f.write(content)
		f.close()
	except:
		pass


def print_table_row(dom_node):
	row = ""
	td_nodes = dom_node.childNodes
	for td in td_nodes:
		if td.nodeName == "td" or td.nodeName == "th":
				if td.firstChild.nodeName == "#text" :
					row += " " + td.firstChild.nodeValue
	return row

def parse_table(html_content):
	table_text = ""
	try:
		table_dom = parseString("<?xml version=\"1.0\" encoding=\"utf-8\"?>"+html_content)	
		table = table_dom.firstChild
		nodes = table.childNodes
		
		for tr in nodes:
			if tr.nodeName == "tr":
				table_text += print_table_row(tr)
				table_text += "\n"
	except:
		pass;

	return table_text

def get_stock_struct_data(content):
	table = re.match("[\s\S]*?(<table\sid=\"lngbbd_Table\">[\s\S]*?</table>)[\s\S]*", content)
	if table :
		ntable = string.replace(table.group(1), "&nbsp;", "")
		data_txt = parse_table(ntable)
		if len(data_txt) > 0:
			return data_txt

def get_stock_struct(stock_code, url):
	content = wget2(url)
	data = get_stock_struct_data(content)
#	print data.encode("utf8")

	return data

def save_stock_struct(stock_code, data, dir):
	file_name = dir + "/" + stock_code
	file = open(file_name, "w")
	file.write(data)
	file.close()


web="http://f10.eastmoney.com/f10_v2/CapitalStockStructure.aspx?code=sz000001"
save_dir = "../../../data/stock_struct/eastmoney"
if __name__ == "__main__":
	stocks = read_stock("sh") 
	print len(stocks)
#	for k,v in stocks.items():
#		url = "http://f10.eastmoney.com/f10_v2/CapitalStockStructure.aspx?code=sh{0}".format(k)
#		print url
#		save(k, get_stock_struct(k, url), save_dir)
#
	stocks = read_stock("sz") 
	print len(stocks)
	i=0
	for k,v in stocks.items()[500:]:
		url = "http://f10.eastmoney.com/f10_v2/CapitalStockStructure.aspx?code=sz{0}".format(k)
		print i, url
		save(k, get_stock_struct(k, url), save_dir)

		i+=1
