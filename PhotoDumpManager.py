import os.path
import os, time

dumpDirectory = '/Users/bbeau/Pictures/Dump/RAW/'
exitDirectory = '/Users/bbeau/Downloads/test/'

for filename in os.listdir(dumpDirectory):
    print(time.ctime(os.path.getmtime(dumpDirectory+filename)))