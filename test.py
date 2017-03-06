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

def cacher(lines, targetDate, measurement):
    totalbytesserved = []
    #totalbytesfromcache = []
    totalbytesfromorigin = []
    totalbytesfrompeers = []
    if measurement == 'Logs':
        print "Using Logs"
        for x in lines:
            datestr, timestr, logmsg = (x.split(' ', 2) + ['', '', ''])[:3]
            if datestr == targetDate:
                linesplit = str.split(logmsg)
                # Search through the log for completed transactions (served all)
                if 'Served all' in logmsg:
                    total_served_size = linesplit[3]
                    total_served_bwtype = linesplit[4]
                    #fromcache_size = linesplit[8]
                    #fromcachebwtype = linesplit[9]
                    fromorigin_size = linesplit[12]
                    fromoriginbwtype = linesplit[13]
                    frompeers_size = linesplit[17]
                    frompeersbwtype = linesplit[18]
                    # Convert size of from cache to bytes
                    if total_served_bwtype == 'KB':
                        bytes_served = "%.0f" % (
                            float(total_served_size) * 1024)
                    elif total_served_bwtype == 'MB':
                        bytes_served = "%.0f" % (
                            float(total_served_size) * 1048576)
                    elif total_served_bwtype == 'GB':
                        bytes_served = "%.0f" % (
                            float(total_served_size) * 1073741824)
                    elif total_served_bwtype == 'TB':
                        bytes_served = "%.0f" % (
                            float(total_served_size) * 1099511627776)
                    elif total_served_bwtype == 'bytes':
                        bytes_served = total_served_size
                    # Convert size of from internet(origin) to bytes
                    if fromoriginbwtype == 'KB':
                        bytesfromorigin = "%.0f" % (float(fromorigin_size) * 1024)
                    elif fromoriginbwtype == 'MB':
                        bytesfromorigin = "%.0f" % (float(fromorigin_size) * 1048576)
                    elif fromoriginbwtype == 'GB':
                        bytesfromorigin = "%.0f" % (float(fromorigin_size) * 1073741824)
                    elif fromoriginbwtype == 'TB':
                        bytesfromorigin = "%.0f" % (float(fromorigin_size) * 1099511627776)
                    elif fromoriginbwtype == 'bytes':
                        bytesfromorigin = fromorigin_size
                    # Convert size of from peers to bytes
                    if frompeersbwtype == 'KB':
                        bytesfrompeers = "%.0f" % (float(frompeers_size) * 1024)
                    elif frompeersbwtype == 'MB':
                        bytesfrompeers = "%.0f" % (float(frompeers_size) * 1048576)
                    elif frompeersbwtype == 'GB':
                        bytesfrompeers = "%.0f" % (float(frompeers_size) * 1073741824)
                    elif frompeersbwtype == 'TB':
                        bytesfrompeers = "%.0f" % (float(frompeers_size) * 1099511627776)
                    elif frompeersbwtype == 'bytes':
                        bytesfrompeers = frompeers_size
                   
                    # Append each bw size to the total count
                    totalbytesserved.append(bytes_served)
                    totalbytesfromorigin.append(bytesfromorigin)
                    totalbytesfrompeers.append(bytesfrompeers)
                # Search through the logs for incomplete transactions (served)
                if 'Served all' not in logmsg and 'Served' in logmsg:
                    total_served_size = linesplit[2]
                    total_served_bwtype = linesplit[3]
                    #fromcache_size = linesplit[8]
                    #fromcachebwtype = linesplit[9]
                    fromorigin_size = linesplit[11]
                    fromoriginbwtype = linesplit[12]
                    frompeers_size = linesplit[16]
                    frompeersbwtype = linesplit[17]
                    # Convert size of from cache to bytes
                    if total_served_bwtype == 'KB':
                        bytes_served = "%.0f" % (
                            float(total_served_size) * 1024)
                    elif total_served_bwtype == 'MB':
                        bytes_served = "%.0f" % (
                            float(total_served_size) * 1048576)
                    elif total_served_bwtype == 'GB':
                        bytes_served = "%.0f" % (
                            float(total_served_size) * 1073741824)
                    elif total_served_bwtype == 'TB':
                        bytes_served = "%.0f" % (
                            float(total_served_size) * 1099511627776)
                    elif total_served_bwtype == 'bytes':
                        bytes_served = total_served_size
                    # Convert size of from internet(origin) to bytes
                    if fromoriginbwtype == 'KB':
                        bytesfromorigin = "%.0f" % (float(fromorigin_size) * 1024)
                    elif fromoriginbwtype == 'MB':
                        bytesfromorigin = "%.0f" % (float(fromorigin_size) * 1048576)
                    elif fromoriginbwtype == 'GB':
                        bytesfromorigin = "%.0f" % (float(fromorigin_size) * 1073741824)
                    elif fromoriginbwtype == 'TB':
                        bytesfromorigin = "%.0f" % (float(fromorigin_size) * 1099511627776)
                    elif fromoriginbwtype == 'bytes':
                        bytesfromorigin = fromorigin_size
                    # Convert size of from peers to bytes
                    if frompeersbwtype == 'KB':
                        bytesfrompeers = "%.0f" % (float(frompeers_size) * 1024)
                    elif frompeersbwtype == 'MB':
                        bytesfrompeers = "%.0f" % (float(frompeers_size) * 1048576)
                    elif frompeersbwtype == 'GB':
                        bytesfrompeers = "%.0f" % (float(frompeers_size) * 1073741824)
                    elif frompeersbwtype == 'TB':
                        bytesfrompeers = "%.0f" % (float(frompeers_size) * 1099511627776)
                    elif frompeersbwtype == 'bytes':
                        bytesfrompeers = frompeers_size
                    # Append each bw size to the total count
                    totalbytesserved.append(bytes_served)
                    totalbytesfromorigin.append(bytesfromorigin)
                    totalbytesfrompeers.append(bytesfrompeers)
    elif measurement == 'DB':
        print "Using DB"
        print " Getting date range in epoch for target date: %s" % targetDate


    totalbytesserved = sum(map(int, totalbytesserved))
    totalbytesfromorigin = sum(map(int, totalbytesfromorigin))
    totalbytesfrompeers = sum(map(int, totalbytesfrompeers))
    
    print "Total Bytes from cache: %s" % convert_bytes_to_human_readable(totalbytesserved)
    print "Total Bytes from origin: %s" % convert_bytes_to_human_readable(totalbytesfromorigin)
    print "Total Bytes from peers: %s" % convert_bytes_to_human_readable(totalbytesfrompeers)




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


def main():
    
    # Options
    usage = '%prog [options]'
    o = optparse.OptionParser(usage=usage)
    o.add_option('--targetdate',
                 help=('Optional: Date to parse. Example: 2017-01-15.'))
    o.add_option('--logpath',
                 help=('Optional: Caching Log Path. Defaults to: '
                       '/Library/Server/Caching/Logs'))
    o.add_option('--deviceids',
                 help='Optional: Use Device IDs (Ex: iPhone7,2). Defaults'
                 ' to: False',
                 action='store_true')
    o.add_option('--nostdout',
                 help='Optional: Do not print to standard out',
                 action='store_true')
    o.add_option('--configureserver',
                 help='Optional: Configure Server to log Client Data',
                 action='store_true')
    o.add_option('--serveralert',
                 help='Optional: Send Server Alert',
                 action='store_true')
    o.add_option("--slackalert", action="store_true", default=False,
                 help=("Optional: Use Slack"))
    o.add_option("--slackwebhook", default=None,
                 help=("Optional: Slack Webhook URL. Requires Slack Option."))
    o.add_option("--slackusername", default=None,
                 help=("Optional: Slack username. Defaults to Cacher."
                       "Requires Slack Option."))
    o.add_option("--measurement", default=None,
                 help=("Optional: Measurement method to use."
                       "Either DB or Logs, defaults to logs"))
    o.add_option("--slackchannel", default=None,
                 help=("Optional: Slack channel. Can be username or channel "
                       "Ex. #channel or @username. Requires Slack Option."))

    opts, args = o.parse_args()

    if opts.measurement:
        measurement = opts.measurement
    else:
        measurement = 'Logs'

    targetDate = "2017-02-21"
    logPath = '/Library/Server/Caching/Logs'

    try:
        os.remove(os.path.join(logPath, '.DS_Store'))
    except OSError:
        pass
    if not os.listdir(logPath):
        print 'Cacher did not detect log files in %s' % logPath
        sys.exit(1)

    # Make temporary directory
    tmpDir = tempfile.mkdtemp()

    # Clone the contents of serverlogs over into the 'cachinglogs' subdirectory
    tmpLogs = os.path.join(tmpDir, 'cachinglogs')
    shutil.copytree(logPath, tmpLogs)

    # Expand any .bz files in the directory (Server 4.1+)
    os.chdir(tmpLogs)
    for bzLog in glob.glob(os.path.join(tmpLogs, '*.bz2')):
        result = subprocess.check_call(["bunzip2", bzLog])
    # Now combine all .log files in the destination into a temp file that's
    # removed when python exits
    rawLog = tempfile.TemporaryFile()
    # We only care about Debug logs, not service logs
    for anyLog in glob.glob(os.path.join(tmpLogs, 'Debug*')):
        with open(anyLog, 'rb') as f:
            shutil.copyfileobj(f, rawLog)

    # Skip back to the beginning of our newly concatenated log
    rawLog.seek(0)

    # Purge temporary directory since it's now in memory.
    shutil.rmtree(tmpDir)

    cacherdata = cacher(rawLog.readlines(), targetDate, measurement)



if __name__ == '__main__':
    main()









