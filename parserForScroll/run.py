#!/usr/bin/python

import os
import sys
import re

dis = [8, 10, 12, 14, 16]

for i in range(2,len(sys.argv)):
    pwd = sys.argv[i] + '/'
    ls = os.listdir(pwd)
    new_pwd = pwd + "parsed_data/"
    if not os.path.isdir(new_pwd):
        os.system("mkdir " + new_pwd)
    for filename in ls:
        if filename.startswith('.') or re.search('UIInternalEvent', filename):
            continue
        if not re.search('Scroll', filename):
            continue
        
        filename2 = "UIInternalEvent " + filename

        os.system("cp '" + pwd + filename + "' " + new_pwd)
        os.system("cp '" + pwd + filename2 + "' " + new_pwd)

        out_filename = "'" +new_pwd + "Scroll" + filename + "'"
        out_filename2 = "'Scroll" + filename[:-4] + ".csv'"
#         out_filename2 = "'Scroll_5_times_" + filename[:-4] + ".csv'"
        filename = "'" + new_pwd + filename + "'"
        filename2 = "'" + new_pwd + filename2 + "'"

        os.system("sed -e '/move/d' -e '/end/d' -e '/scroll/d' " + filename + " > aa.txt")
#         os.system("sed -e '/Complete/d' -e '/move/d' -e '/end/d' -e '/scroll/d' " + filename + " | ./count.py > aa.txt")
        os.system("sed -e '/stationary/d' " + filename2 + " >> aa.txt")
        os.system("sort -k 1 aa.txt > bb.txt")
        os.system("./cc.py bb.txt > cc.txt")
        os.system("sort -k 1 cc.txt > dd.txt")
        if sys.argv[1] != "main_distance.rb":
            print sys.argv[1]
            os.system("ruby-1.9.2-p318 " + sys.argv[1] + " dd.txt > '" + new_pwd + out_filename2[1:])
        else:
            print sys.argv[1]
            for d in dis:
                os.system("ruby-1.9.2-p318 main_distance.rb dd.txt " + str(d) + " > '" + new_pwd + str(d) + "_" + out_filename2[1:])
#         os.system("rm aa.txt bb.txt cc.txt dd.txt")
#         os.system('./seperateMultiTouchParser.py ' + filename + ' |./seperateSameTimeParser.py | ./preParserForCSV.py ' + filename )
#         os.system('./logParserForCSV ' + filename[:-5] + "(parsed).txt'")
#         os.system('./postParserForCSV.py ' + filename[:-5] + "(parsed).csv'")
