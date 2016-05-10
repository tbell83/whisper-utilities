#!/usr/bin/python
import argparse
import os
import time
from prettytable import PrettyTable

parser = argparse.ArgumentParser()
parser.add_argument('-a', action='store', dest='age', type=int, default=30)
parser.add_argument('-p', action='store', dest='path', type=str,
                    default='/opt/graphite/storage/whisper/applications')
parser.add_argument('-l', action='store_true', dest='listMetrics',
                    default=False)
parser.add_argument('-t', action='store_false', dest='showTable',
                    default=True)
args = parser.parse_args()

graphiteDirectory = args.path
showTable = args.showTable
listMetrics = args.listMetrics
age = args.age * (24 * 60 ** 2)
epochTarget = int(time.time()) - age

applications = os.listdir(graphiteDirectory)

table = PrettyTable(["Metric Path", "Files", "Size (MB)"],
                    padding_width=2,
                    sortby='Size (MB)',
                    reversesort=True)
table.align = "l"

totalMetrics = 0
totalSize = 0

for application in applications:
    size = 0
    fileCount = 0
    for root, dirs, files in os.walk(graphiteDirectory + '/' + application):
        for file in files:
            if os.path.getmtime(root + '/' + file) < epochTarget:
                fileCount += 1
                size += os.path.getsize(root + '/' + file)
                if listMetrics:
                    print root + file
    result = {'size': size, 'files': fileCount}
    totalSize += size
    totalMetrics += fileCount
    if size / 1024 ** 2 > 0:
        table.add_row([
                      application,
                      fileCount,
                      size / 1024 ** 2])

if showTable:
    print table
    print '{} unused metrics totalling {} GB'.format(totalMetrics,
                                                     totalSize / 1024 ** 3)
