#!/usr/bin/python

count = 0
while True:
    try:
        line = raw_input()
    except EOFError:
        break

    s = line.split()
    if s[0] != 'Complete':
        try:
            if s[2] == 'start' or s[2] == "time's":
                count = 0
                print line
            elif s[1] == '-1':
                print line
            elif s[2] == 'begin' and count < 5:
                count = count + 1
                print line
            elif s[1] != '-1' and count < 5:
                print line
            elif s[1] != '-1' and count == 5 and s[2] == 'end':
                count = count + 1
                print line
        except:
            print line
