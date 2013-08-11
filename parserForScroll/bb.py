#!/usr/bin/python

import sys
import re

file_name = open(sys.argv[1], 'r')

p_done = re.compile('done')
taskID = ['19','13','22','24','29','28','18','19','17','27','22','23','12','18','14','28','21']
taskNum = 0

for line in file_name:
    line = line[:-1]
    if taskNum == 0:
        data = line.split()
        print data[0] + ' -9 -9 start ' + taskID[taskNum]
        taskNum = 1
    print line
    if re.search(p_done, line) and taskNum < len(taskID):
        data = line .split()
        print data[0] + ' -9 -9 start ' + taskID[taskNum]
        taskNum = taskNum + 1
