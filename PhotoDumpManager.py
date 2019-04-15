import os.path, os, time, sys
from shutil import copy2

if(len(sys.argv) < 3):
    raise AttributeError('Please provide path for dump and exit directories.')

dumpDirectory = sys.argv[1]
exitDirectory = sys.argv[2]
filePath = ''

if not os.path.exists(dumpDirectory):
    raise ValueError('No directory at '+dumpDirectory+'.')
if not os.path.exists(exitDirectory):
    raise ValueError('No directory at '+exitDirectory+'.')

if not dumpDirectory[-1:] == os.sep:
    dumpDirectory += os.sep

if not exitDirectory[-1:] == os.sep:
    exitDirectory += os.sep

for fileName in os.listdir(dumpDirectory):
    fileTimestamp = time.strftime("%Y-%B-%d", time.localtime(os.path.getmtime(dumpDirectory+fileName))).split('-')
    fileTimestamp.insert(0, fileName.split('.')[1])
    filePath = exitDirectory
    for text in fileTimestamp:
        filePath += text + os.sep
        if not os.path.exists(filePath):
            os.makedirs(filePath)
    if not os.path.exists(filePath + fileName):
        print('Moving file ' + dumpDirectory + fileName + ' to ' + filePath + fileName)
        copy2(dumpDirectory + fileName, filePath + fileName)
    