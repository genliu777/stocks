#!/usr/bin/python
import sys
import os
import dircache
file_path = sys.argv[1]
script = sys.argv[2]
which_day = sys.argv[3]

#print file_path, script

files = os.listdir(file_path)

for file in files:
	full_file_path = "{0}/{1}".format(file_path, file)
	st = os.stat(full_file_path)
#	print full_file_path, st
	if script:
#		print script, full_file_path
		os.system("{0} {1} {2}".format(script, full_file_path, which_day))
