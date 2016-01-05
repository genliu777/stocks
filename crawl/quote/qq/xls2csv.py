#!/usr/bin/env python
import sys
import string
import xlrd
import codecs

def row2str(row):
	s = []
	for cell in row:
		if type(cell) == unicode :
			s.append(cell)
		else:
			s.append(str(cell))	

	return string.join(s, ",")

def xls2csv_lines(xls):
	data = xlrd.open_workbook(xls)
	table = data.sheets()[0]
	nrows = table.nrows
	nclos = table.ncols
	lines = []

	for i in range(nrows):
		row = table.row_values(i)
		s = row2str(row)
		lines.append(s)

	return lines

def xls2csv(xls, csv):
	data = xlrd.open_workbook(xls)
	table = data.sheets()[0]
	nrows = table.nrows
	nclos = table.ncols

	if csv != None:
		csv_file = codecs.open(csv, "w", "utf8")

	for i in range(nrows):
		row = table.row_values(i)
		s = row2str(row)
		if csv:
			csv_file.write(s+"\n")	
		else:
			print s + "\n"

	if csv:
		csv_file.close()

if __name__ == "__main__":
	xls2csv("2016-01-04.xls", "2016-01-04.csv")
