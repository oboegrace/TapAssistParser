#!/usr/bin/python

import sys
import re

def distance(targetX, targetY, x, y):
    return ((targetX-x)**2+(targetY-y)**2)**0.5

fin = open(sys.argv[1], 'r')

pattern = re.compile('([-0-9]+) (move|begin|end|start) ([-0-9]+) ([-0-9]+)')

touches = {}
d = 20000
intendedTouch = 0
targetX = 0
targetY = 0

for line in fin:
    line = line[:-1]
    m = re.search(pattern, line)
    if m:
        if m.group(2) == 'begin':
            touches[m.group(1)] = [line]
            tempD = distance(targetX,targetY,int(m.group(3)),int(m.group(4)))
            print line
            if tempD < d:
                d = tempD
                intendedTouch = m.group(1)
        elif m.group(2) == 'end' and m.group(1) != '-1':
            if m.group(1) == intendedTouch:
                d = 20000
                for l in touches[m.group(1)]:
                    print l
                print line
        elif m.group(2) == 'move':
            touches[m.group(1)].append(line)
        elif m.group(2) == 'start':
            targetX = int(m.group(3))
            targetY = int(m.group(4))
            print line
    else:
        print line
