#!/usr/bin/python

count = 0
while True:
    try:
        line = raw_input()
    except EOFError:
        break

    s = line.split()
    if s[2] == 'done' or s[2] == "time's":
        count = 0
        print line
    elif s[2] == 'begin' and count < 5:
        count = count + 1
        print line
