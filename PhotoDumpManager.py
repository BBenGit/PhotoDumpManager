import os.path, os, time, sys
from shutil import copy2

if(len(sys.argv) < 3):
    raise AttributeError('Please provide path for dump and exit directories.')

dumpDirectory = sys.argv[1]
exitDirectory = sys.argv[2]
filepath = ''

if not os.path.exists(exitDirectory):
    raise ValueError('No directory at '+dumpDirectory+'.')
if not os.path.exists(exitDirectory):
    raise ValueError('No directory at '+exitDirectory+'.')

for filename in os.listdir(dumpDirectory):
    test = time.strftime("%Y-%B-%d", time.localtime(os.path.getctime(dumpDirectory+filename))).split('-')
    filepath = exitDirectory
    for i in range(3):
        filepath += test[i] + '/'
        if not os.path.exists(filepath):
            os.makedirs(filepath)
    if not os.path.exists(filepath + filename):
        copy2(dumpDirectory + filename, filepath + filename)
    