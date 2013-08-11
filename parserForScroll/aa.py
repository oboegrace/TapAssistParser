#!/usr/bin/python

import sys
import re

file_name = open(sys.argv[1], 'r')

p_start = re.compile('start')
p_begin = re.compile('begin')
p_end = re.compile('end')
p_cancel = re.compile('cancel')

dataDict = {}

for line in file_name:
    if re.search(p_start, line):
        data = line.split()
        
    if re.search(p_begin, line):
        log = line.split()
        tmpDict = {}
        tmpDict['timestamp'] = log[0]
        tmpDict['logs'] = [log]
        dataDict[log[1]] = tmpDict
    print line
