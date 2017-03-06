#!/usr/bin/python

from datetime import date, timedelta
from distutils.version import LooseVersion
import glob
import json
import logging
import optparse
import os
import plistlib
import re
import shutil
import subprocess
import sys
import tempfile
import urllib2
import time
import sqlite3

def convert_bytes_to_human_readable(number_of_bytes):
    if number_of_bytes < 0:
        raise ValueError("ERROR: number of bytes can not be less than 0")

    step_to_greater_unit = 1024.
    number_of_bytes = float(number_of_bytes)
    unit = 'bytes'
    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'KB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'MB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'GB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'TB'

    precision = 1
    number_of_bytes = round(number_of_bytes, precision)
    return str(number_of_bytes) + ' ' + unit


DB_PATH = '/Library/Server/Caching/Logs/Metrics.sqlite'

date_given = '2017-02-23'
date_time_start = date_given + ':00.00:01'
date_time_stop =  date_given + ':23.59:59'
pattern_start = '%Y-%m-%d:%H.%M:%S'
pattern_stop = '%Y-%m-%d:%H.%M:%S'
epoch_start = int(time.mktime(time.strptime(date_time_start, pattern_start)))
epoch_stop = int(time.mktime(time.strptime(date_time_stop, pattern_stop)))



print "Epoch Start: %s" % epoch_start
print "Epoch Stop:  %s" % epoch_stop
print ' '


print " - Opening Database ..."
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
print " - Getting values"
c.execute("SELECT dataValue FROM statsData WHERE metricName LIKE 'bytes.fromorigin.toclients' AND collectionDate > '%s' AND collectionDate < '%s'" % (epoch_start, epoch_stop))
bytes_fromorigin = c.fetchall()
print " "
print "Results: "
total_bytes = []
for bytes in bytes_fromorigin:
    total_bytes.append(bytes[0])
    print bytes[0]

print "Total bytes: %s" % convert_bytes_to_human_readable(sum(map(int,total_bytes)))






#Epoch Start: 1487768401
#Epoch Stop:  1487854799




