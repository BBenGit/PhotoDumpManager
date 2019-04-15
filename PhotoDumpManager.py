#!/usr/bin/env python3

# Copyright 2019 Benjamin Beau <fnounfoun@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

import os
import time
from shutil import copy2
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-directory", "-i", type=str, required=True, help="Directory where to find input images")
    parser.add_argument(
        "--output-directory", "-o", type=str, required=True, help="Directory where to put destination files"
    )
    args = parser.parse_args()

    dumpDirectory = args.input_directory
    exitDirectory = args.output_directory
    filePath = ''

    if not os.path.exists(dumpDirectory):
        raise ValueError('No directory at ' + dumpDirectory + '.')
    if not os.path.exists(exitDirectory):
        raise ValueError('No directory at ' + exitDirectory + '.')

    if not dumpDirectory[-1:] == os.sep:
        dumpDirectory += os.sep

    if not exitDirectory[-1:] == os.sep:
        exitDirectory += os.sep

    for fileName in os.listdir(dumpDirectory):
        if os.path.isfile(fileName):
            fileTimestamp = time.strftime("%Y-%B-%d", time.localtime(os.path.getmtime(dumpDirectory + fileName))).split('-')
            fileTimestamp.insert(0, fileName.split('.')[1])
            filePath = exitDirectory
            for text in fileTimestamp:
                filePath += text + os.sep
                if not os.path.exists(filePath):
                    os.makedirs(filePath)
            if not os.path.exists(filePath + fileName):
                print('Moving file ' + dumpDirectory + fileName + ' to ' + filePath + fileName)
                copy2(dumpDirectory + fileName, filePath + fileName)
