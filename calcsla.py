'''
Created on Feb 10, 2017

@author: inagakii
'''
#coding: utf-8
from datetime import *
from dateutil.relativedelta import *
import csv
import codecs
from jpbizcalendar import *

CSV_IN_FILE = '/Users/inagakii/Documents/dwh/metrics data/2016/case_jp_20160101_20161113.txt'
CSV_OUT_FILE = '/Users/inagakii/Documents/dwh/metrics data/2016/case_jp_20160101_20161113_adjusted.txt'
COL_CASE_ID = 'caseid'
COL_SEVERITY = 'severity'
COL_CREATION_UTC = 'creation_utc'
COL_FIRSTRES_UTC = 'firstresponse_utc'
COL_QUEUE = 'queue'
COL_IS_SLA_MET_EMAIL ='is_sla_met_email'
QUEUE_DEVELOPER = 'developer'
QUEUE_TIER1 = 'tier1'

SLA_TIME = 0, 60, 240, 720, 1440, 15

print(u'helloworld')

bizcal = JpBizCalendar(2016, 'UTC')

#TEST
#tmpstart = datetime(2016,3,1,7,3,0)
#bizcal.get_jst(tmpstart)
#tmpend = datetime(2016,3,3,0,40,0)
#tmpelapse = bizcal.get_business_elapse(tmpstart, tmpend)
#print(tmpelapse)

infile = codecs.open(CSV_IN_FILE, 'r', 'utf_8')
outfile = codecs.open(CSV_OUT_FILE, 'w', 'utf_8')
reader = csv.reader(infile, delimiter='\t')
writer = csv.writer(outfile, delimiter='\t', quoting=csv.QUOTE_MINIMAL)

header = next(reader)
ccolumn = 0
for column in header:
    print (column)
    if column == COL_CASE_ID:
        idxcase=ccolumn
    elif column == COL_SEVERITY:
        idxseverity=ccolumn
    elif column == COL_CREATION_UTC:
        idxcrutc=ccolumn
    elif column == COL_FIRSTRES_UTC:
        idxfrutc=ccolumn
    elif column == COL_QUEUE:
        idxqueue=ccolumn
    elif column == COL_IS_SLA_MET_EMAIL:
        idxisslametemail=ccolumn
        break
    ccolumn = ccolumn + 1

header.append('is_adjusted_missed')
header.append('biz_elapse_min')

writer.writerow(header)

crow = 0
for row in reader:
    #print(row)
    if QUEUE_DEVELOPER in row[idxqueue] or QUEUE_TIER1 in row[idxqueue]:
        crutc = datetime.strptime(row[idxcrutc], "%Y-%m-%d %H:%M:%S")
        if row[idxfrutc] is not '':
            frutc = datetime.strptime(row[idxfrutc], "%Y-%m-%d %H:%M:%S")
            elapsemin = bizcal.get_business_elapse(crutc, frutc)
            if SLA_TIME[int(row[idxseverity])] > elapsemin:
                row.append(0)
            else:
                row.append(1)
            row.append(elapsemin)
        else:
            row.append(1)
        print(row)
    else:
        if int(row[idxisslametemail]) > 0: 
            row.append(0)
        else:
            row.append(1)
    writer.writerow(row)
    crow=crow + 1

infile.close()
outfile.close()
