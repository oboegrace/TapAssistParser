#!/usr/bin/python

import re

pattern1 = re.compile('([-0-9]+\.\d+)+ (\d+) (move|begin|end) (\d)+ (\d)+')
pattern2 = re.compile('([-0-9]+\.\d+)+ (.+)')

lastTime = 0
logLine = []

while True:
    try:
        line = raw_input()
    except EOFError:
        break

    m = re.search(pattern1, line)
    if m:
        if m.group(3) == 'begin':
            lastTime = m.group(1)
            logLine = [line]
        elif m.group(3) == 'move':
            if lastTime == m.group(1):
                logLine.append(line)
            else:
                if len(logLine) > 1:
                    for i in range(0,len(logLine)):
                        logLine[i] = re.sub(pattern2, '\g<1>'+str(int(10/float(len(logLine))*i))+' \g<2>', logLine[i])
                        print logLine[i]
                elif len(logLine) == 1:
                    print logLine[0]
                lastTime = m.group(1)
                logLine = [line]
        elif m.group(3) == 'end':
            printEndYet = False
            if lastTime == m.group(1):
                logLine.append(line)
                printEndYet = True
            if len(logLine) > 1:
                for i in range(0,len(logLine)):
                    logLine[i] = re.sub(pattern2, '\g<1>'+str(int(10/float(len(logLine))*i))+' \g<2>', logLine[i])
                    print logLine[i]
            elif len(logLine) == 1:
                print logLine[0]
            if not printEndYet:
                print line
    else:
        print line
