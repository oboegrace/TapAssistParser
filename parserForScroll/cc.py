#!/usr/bin/python

import sys
import re

file_name = open(sys.argv[1])

pattern = re.compile('(\d+\.\d+)(.*)(\d+) (begin|move|end|cancel) [-0-9]+ [-0-9]+ ([0-9.]+)') 
p_begin = re.compile('(\d+\.\d+) \d+ begin')

touches = {}

for line in file_name:
    line = line[:-1]
    m = re.search(pattern, line)
    try:
        if m:
            if m.group(4) == 'begin':
                if m.group(2) != ' ':
                    tmpDict = {}
                    tmpDict['inTableView'] = False
                    tmpDict['timestamp'] = m.group(1)
                    tmpDict['pressure'] = m.group(5)
                    tmpDict['logs'] = [line]
                    touches[m.group(3)] = tmpDict
                else:
                    for touch in touches:
                        #Same Event in UIInternal and baseview log data has different timestamp.
                        if m.group(1)[:-4] == touches[touch]['timestamp'][:-4] and int(m.group(1)[-2:])-int(touches[touch]['timestamp'][-2:]) <= 1 and m.group(5) == touches[touch]['pressure']:
                            touches[touch]['inTableView'] = True
            elif m.group(4) == 'end':
                if touches[m.group(3)]['inTableView']:
                    for l in touches[m.group(3)]['logs']:
                        print l
                    print line
            else:
                touches[m.group(3)]['logs'].append(line)
        else:
            print line
    except:
        print "BUG: " + line
