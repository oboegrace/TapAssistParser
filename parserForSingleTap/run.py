#!/usr/bin/python

import os
import sys
import re

for i in range(1,len(sys.argv)):
    pwd = sys.argv[i] + '/'
    ls = os.listdir(pwd)
    new_pwd = pwd + "parsed_data/"
    if not os.path.isdir(new_pwd):
        os.system("mkdir " + new_pwd)
    for filename in ls:
        if filename.startswith('.') or re.search('UIInternalEvent', filename):
            continue
        if not re.search('Single Tap', filename):
            continue
        
        os.system("cp '" + pwd + filename + "' " + new_pwd)
        filename = "'" + new_pwd + filename + "'"
        os.system('./seperateMultiTouchParser.py ' + filename + ' |./seperateSameTimeParser.py | ./preParserForCSV.py ' + filename )
#         os.system('./seperateMultiTouchParser.py ' + filename + ' |./seperateSameTimeParser.py | ./count.py | ./preParserForCSV.py ' + filename )
        os.system('./logParserForCSV ' + filename[:-5] + "(parsed).txt'")
        os.system('./postParserForCSV.py ' + filename[:-5] + "(parsed).csv'")
