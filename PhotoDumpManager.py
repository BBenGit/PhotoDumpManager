import os.path, os, time, sys
from shutil import copy2

if(len(sys.argv) < 3):
    raise AttributeError('Please provide path for dump and exit directories.')

dumpDirectory = sys.argv[1]
exitDirectory = sys.argv[2]
filePath = ''
fileExt = ''

if not os.path.exists(exitDirectory):
    raise ValueError('No directory at '+dumpDirectory+'.')
if not os.path.exists(exitDirectory):
    raise ValueError('No directory at '+exitDirectory+'.')

if not dumpDirectory[-1:] == os.sep:
    dumpDirectory += os.sep

if not exitDirectory[-1:] == os.sep:
    exitDirectory += os.sep

for filename in os.listdir(dumpDirectory):
    test = time.strftime("%Y-%B-%d", time.localtime(os.path.getmtime(dumpDirectory+filename))).split('-')
    test.insert(0, filename.split('.')[1])
    filePath = exitDirectory
    for text in test:
        filePath += text + os.sep
        if not os.path.exists(filePath):
            os.makedirs(filePath)
    if not os.path.exists(filePath + filename):
        copy2(dumpDirectory + filename, filePath + filename)
    