#!/usr/bin/python

import re
import sys

# file_name = raw_input("filename:")
file_name = sys.argv[1]
# f = open(file_name, 'r')
out_file_name = file_name[:-4]+'(parsed).txt'
fout = open(out_file_name, "w")

time_flag = False
start_flag = False
# for line in f:
while True:
    try:
        line = raw_input()
        line = line + '\n'
    except EOFError:
        break
    if re.search("time's", line):
        time_flag = True
        time_line = line
        continue
    if re.search("start", line) and time_flag:
        time_flag = False
        start_flag = True
        start_line = line
        continue
    fout.write(str(line))
    if re.search("end", line) and start_flag:
        start_flag = False
        fout.write(str(time_line))
        fout.write(str(start_line))

# f.close()
fout.close()
print "output to " + out_file_name + " successfully"
