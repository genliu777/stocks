#!/usr/bin/python
# transport a table in txt for R

import sys
import string
import re

def usage():
	print '''
T.py input_file output_file
'''

def T(input, output):
	txt = open(input, "r")
	lines = txt.readlines()
	txt.close()
	table = []	
	for line in lines:
		tline = re.sub("\s+", " ", line)
		column = string.split(tline, " ")
		table.append(column)

	l_column = len(table)
	l_row = len(table[0])
	for row in table:
		if l_row < len(row):
			l_row = len(row)

	#has table head
	if len(table[0]) < l_row:
		table[0].insert(0, " ")

	output_txt = open(output, "w")
	for j in range(0, l_row):
		for i in range(0, l_column):
			print table[i][j],
			output_txt.write(table[i][j]+" ")
		print "\n",
		output_txt.write("\n")
	output_txt.close()
	

if __name__ == "__main__":
	if len(sys.argv) < 3:
		usage()
		exit(1)
	T(sys.argv[1], sys.argv[2])
