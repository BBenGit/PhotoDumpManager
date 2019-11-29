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

import argparse
import logging
import os
import time
import calendar
from datetime import datetime
from pathlib import Path
from shutil import copy2

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

iterator = 1
count = 0

def sort(inner_directory, output_directory, types, recursive):
    global iterator
    global count
    for filename in os.listdir(inner_directory):
        if not filename.startswith('.'): # Ignore hidden files
            if os.path.isfile(os.path.join(inner_directory, filename)):
                access_time = datetime.fromtimestamp(
                    time.mktime(time.localtime(os.path.getmtime(os.path.join(inner_directory, filename))))
                )
                extension = Path(filename).suffix[1:]  # Remove trailing point between filename and extension

                if extension.lower() in (t.lower() for t in types):
                    # Make subdirectory like: filename/year/month/day
                    file_path = output_directory
                    for subdir_name in (extension, access_time.year, calendar.month_name[access_time.month], access_time.day):
                        file_path = os.path.join(file_path, str(subdir_name))
                        if not os.path.exists(file_path):
                            os.makedirs(file_path)

                    # Copy the image if does not already exists
                    if not os.path.exists(os.path.join(file_path, filename)):
                        input_file, output_file = os.path.join(inner_directory, filename), os.path.join(file_path, filename)
                        logger.info(("{:"+str(len(str(count)))+"}/{} - Copying to {}").format(iterator, count, output_file))
                        copy2(input_file, output_file)
                        iterator += 1
            else:
                if recursive:
                    sort(os.path.join(inner_directory, filename), output_directory, types, recursive)

def file_count(inner_directory, types, recursive):
    global count
    for filename in os.listdir(inner_directory):
        if not filename.startswith('.') and Path(filename).suffix[1:].lower() in (t.lower() for t in types) and os.path.isfile(os.path.join(inner_directory, filename)):
                count += 1

        else:
            if recursive:
                file_count(os.path.join(inner_directory, filename), types, recursive)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--recursive','-r', action='store_true', help='')
    parser.add_argument("--input-directory", "-i", type=str, required=True, help="Directory where to find input images")
    parser.add_argument(
        "--output-directory", "-o", type=str, required=True, help="Directory where to put destination files"
    )
    parser.add_argument('--types','-t', nargs='+', required=True, help='Types of file to be ordered')
    args = parser.parse_args()

    input_directory = args.input_directory
    output_directory = args.output_directory
    types = args.types
    recursive = args.recursive

    if not os.path.exists(input_directory):
        raise NotADirectoryError('No directory at %s.', input_directory)
    if not os.path.exists(output_directory):
        logger.info("Missing output directory at %s. Creating it…", output_directory)
        os.makedirs(output_directory)

    file_count(input_directory, types, recursive)
    sort(input_directory, output_directory, types, recursive)

    
