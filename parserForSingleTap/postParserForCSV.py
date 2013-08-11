#!/usr/bin/python
#coding=utf-8

import re
import os
import sys
import csv, codecs, cStringIO
import numpy

class UnicodeWriter:
    """
        A CSV writer which will write rows to CSV file "f",
        which is encoded in the given encoding.
        """
    
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
        self.nextRowNum = 1
    
    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)
        self.nextRowNum = self.nextRowNum + 1
    
    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

# fin = open(sys.argv[1], 'r')
out_file_name = sys.argv[1][:-4]+'(Errors).csv'
fout = open(out_file_name, "wb")
# fout.write(str('Task Attemp,target_x,target_y,TouchID,touchDown_x,touchDown_y,distToTargetX,distToTargetY,(mm)distToTargetX,(mm)distToTargetY,distToTarget,Touch_Down Inaccuracy,x_to_target center,y_to_target center,Touch_Up Inaccuracy,x_to_target center,y_to_target center,movement,max_x,max_y,min_x,min_y,ave_x,ave_y,SD_x,SD_y,x_up-down,y_up-down,Max_speed,Min_speed,Ave_speed,SD_speed,time > 0.5,duration_time,multi-touch\n'))

csvReader = csv.reader(open(sys.argv[1], 'rb'))
csvWriter = UnicodeWriter(fout)
csvWriter.writerow(['Task','Attemp','target_x','target_y','TouchID','touchDown_x','touchDown_y','distToTargetX','distToTargetY','(mm)distToTargetX','(mm)distToTargetY','Touch_Down Inaccuracy','x_to_target center','y_to_target center','Touch_Up Inaccuracy','x_to_target center','y_to_target center','movement','max_x','max_y','min_x','min_y','ave_x','ave_y','SD_x','SD_y','x_up-down','y_up-down','Max_speed','Min_speed','Ave_speed','SD_speed','time > 0.5','duration_time','multi-touch'])
singleTrial = []
maxLine= []
for row in csvReader:
    # Skip First Line
    if row and row[0] == 'Task':
        continue
    # Detect New Task
    if row and row[0] != '':
        taskNum = row[0]
        targetX = row[1]
        targetY = row[2]
#         if singleTrial:
#             print len(singleTrial)
#         print row[0]
    try:
        if row and row[5] != '':
            singleTrial.append(row)
    except:
        print row
# Detect New Trial
    if row and row[3] != '':
        trialNum = row[3]
    # Detect Max Line
    if row and row[9] == 'MAX':
        maxLine = row
    # Detect End of a Trail
    if row and row[9] == 'MIN':
        n = str(csvWriter.nextRowNum)
#         if len(singleTrial[-1]) >= 25:
#             m = re.search('([-0-9]*) ([-0-9]*)', singleTrial[-1][24])
        touchUpXtoTarget = singleTrial[-1][6]
        touchUpYtoTarget = singleTrial[-1][7]
        try:
            distToTargetXNumpyArray = numpy.array(map(lambda x: int(x[10]), singleTrial))
            distToTargetYNumpyArray = numpy.array(map(lambda x: int(x[11]), singleTrial))
        except:
            print map(lambda x: x[10], singleTrial)
        try:
            speedNumpyArray = numpy.array(map(lambda x: float(x[19]), singleTrial[1:]))
        except:
            print map(lambda x: x[19], singleTrial[1:])

        csvWriter.writerow([taskNum,
                            trialNum,
                            targetX,
                            targetY,
                            singleTrial[0][4],
                            singleTrial[0][6],
                            singleTrial[0][7],
                            '=F'+n+'-C'+n,'=G'+n+'-D'+n,
                            '=H'+n+'*10/52',
                            '=I'+n+'*10/52',
                            str(int(len(singleTrial[0]) >= 24 and singleTrial[0][23] == 'inaccurate')),
                            '=H'+n,
                            '=I'+n,
                            str(int(len(singleTrial[-1]) >= 24 and singleTrial[-1][23] == 'move out')),
                            touchUpXtoTarget,
                            touchUpYtoTarget,
                            str(int(len(singleTrial[1]) >= 24 and singleTrial[1][23] == 'moved')),
                            maxLine[10],
                            maxLine[11],
                            row[10],
                            row[11],
                            str(sum(map(lambda x: int(x[10]), singleTrial))/len(map(lambda x: x[10], singleTrial))),
                            str(sum(map(lambda x: int(x[11]), singleTrial))/len(map(lambda x: x[11], singleTrial))),
                            str(distToTargetXNumpyArray.std()),
                            str(distToTargetYNumpyArray.std()),
                            str(int(singleTrial[-1][10])-int(singleTrial[0][10])),
                            str(int(singleTrial[-1][11])-int(singleTrial[0][11])),
                            maxLine[19],
                            row[19],
                            str(speedNumpyArray.mean()),
                            str(speedNumpyArray.std()),
                            str(int(len(maxLine) >= 24 and maxLine[23] == 'time>0.5s')),
                            maxLine[24] if len(maxLine) >= 25 else '',
                            str(int(singleTrial[0][4] != '0')),
                            ])
        singleTrial = []
            
fout.close()
print "output to " + out_file_name + " successfully"
