#!/usr/bin/python
# coding=gbk

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

sys.path.append("../")
from read_sock_list import read_sse_sock

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
	
class crawl:
	def __init__(self, url, type, deep):	
		self.type = type
		self.deep = deep
		self.downloads = {}
		self.urls = {url:0}

	def download(self):
		for k,v in self.downloads.items():
			print "get file " + k + " save as " + v
			wget(k, v)	
			self.downloads.pop(k)
		pass

	def parse(self, content):
		print len(content)
		s = r"<a href=\"(.*)\">"
		m = re.findall(s, content)
		return m

	def grab(self):
		for k,v in self.urls.items():
			self.urls.pop(k)
			if v>self.deep :
				continue
			s = wget2(k)
			if s == None:
				continue

			m = self.parse(s)
			if m == None :
				continue
			for f in m:
				if f.rfind(self.type)  \
					!= len(f) - len(self.type):
					continue
				if f.find("http") != 0 :
					self.downloads[k+f] = f.replace("/", "_")
				else :
					self.downloads[f] = f.replace("/", "_")

	def run(self):
		while 1:
			if len(self.urls) > 0:
				self.grab()

			print self.downloads

			if len(self.downloads) > 0:
				self.download()
			else:
				break

web="http://data.eastmoney.com"

def save(name, content):
	f = codecs.open(name, "w", "utf-8")
	f.write(content)
	f.close()

def get_pdf(name, content):
	lines = string.split(content, "\n")
	for line in lines:
		if string.find(line, "PDF")!=-1:
			pdf_href = re.match(".*?href=\"([^\"]*)\".*", line)
			if pdf_href:
				pdf_url = pdf_href.group(1)
				wget(web+"/"+pdf_url, name+".pdf")
				break

def get_bulletin(name, url):
	content = wget2(url)	
	text = re.match("[\s\S]*?<pre>([\s\S]*?)</pre>[\s\S]*", content)
	if text :
		save(name, text.group(1))	
		get_pdf(name, content)

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

def get_equity_table(dir, url):
	change_dir(dir)
	content = wget2(url)	

	table = re.match("[\s\S]*?(<table\sid=\"lngbbd_Table\">[\s\S]*?</table>)[\s\S]*", content)
	if table :
		ntable = string.replace(table.group(1), "&nbsp;", "")
		equity_txt = parse_table(ntable)
		if len(equity_txt) > 0:
			save("sock_structure.txt", equity_txt)
	os.chdir("..")

def get_market_history(dir, url):
	change_dir(dir)
	content = wget2(url)	
	if content:
		save("market_history.csv", content)
		print content
	os.chdir("..")

def get_market_history_json(dir, url):
	change_dir(dir)
	content = wget2(url)
	json_content = re.match("historySearchHandler\(([^\)]*?)\)", content)
	
	json_content =  json_content.group(1)
	json_content = string.replace(json_content, "累计", "sum")
	json_content = string.replace(json_content, "至",  "-")
	print json_content
	if json_content:
		his = json.loads(json_content)
		print his
	os.change_dir("..")

if __name__ == "__main__":
	socks = read_sse_sock("../../stock_data/socks/sse_sock_A.txt")	
	url = "http://q.stock.sohu.com/hisHq?code=cn_600886&stat=1&order=D&period=d&callback=historySearchHandler&rt=jsonp&0.5429994754601287"
	get_market_history_json("600886", url)
	exit(0)	

#	print socks
	for k,v in socks.items():
		print v[0], v[1]
		url = "http://f10.eastmoney.com/f10_v2/CapitalStockStructure.aspx?code=sh".format(v[0])
		get_finance_table(v[0], url)
