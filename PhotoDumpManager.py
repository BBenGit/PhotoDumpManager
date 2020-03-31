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
import exifread
import subprocess
from datetime import datetime
from pathlib import Path
from shutil import copy2
from utils.log import init_logger

logger = init_logger(__name__, testing_mode=False)
month_name = ["1 - Janvier", "2 - Février", "3 - Mars", "4 - Avril", "5 - Mai", "6 - Juin", "7 - Juillet",
              "8 - Août", "9 - Septembre", "10 - Octobre", "11 - Novembre", "12 - Décembre"]
video_types = ["avi", "mov", "mkv", "mp4", "gif", "wmv", "jpe"]
image_types = ["jpg", "jpeg", "png", "raw", "nef", "dng", "insp"]


def get_file_name(create_datetime, extension, add_microsecond):
    filename = str(create_datetime.date()) + "_" + str(create_datetime.time()).replace(":", "")

    if add_microsecond < 10:
        filename = filename + "000"
    elif add_microsecond < 100:
        filename = filename + "00"

    return filename + str(add_microsecond) + '.' + extension


def get_file_tags(path):
    with open(path, 'rb') as file:
        try:
            tags = exifread.process_file(file)
        except TypeError:
            logger.error("TypeError while getting files tags for file {}".format(path))
            tags = {}

        file.close()
        return tags


def get_tag(tags, tag_name):
    string = ""
    try:
        tag = tags[tag_name]
        string = str(tag)
    except KeyError:
        logger.error("KeyError for '{}'. Tags list = {}".format(tag_name, tags))
    finally:
        return string


def get_image_create_datetime(path):
    datetime_original = get_cmd_output('exiftool -DateTimeOriginal "' + path + '"', "Date/Time Original")
    create_date = get_cmd_output('exiftool -CreateDate "' + path + '"', "Create Date")

    if datetime_original != "":
        logger.info("Use metadata datetime from tag : DateTimeOriginal")
        test = str(datetime_original).split(' ')
        create_datetime = datetime.fromisoformat(test[0].replace(':', '-') + 'T' + test[1])
    elif create_date != "":
        logger.info("Use metadata datetime from tag : CreateDate")
        test = str(create_date).split(' ')
        create_datetime = datetime.fromisoformat(test[0].replace(':', '-') + 'T' + test[1])
    else:
        create_datetime = get_file_modification_datetime(path)

    return create_datetime


def get_cmd_output(cmd, string_prefix):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()

    result = str(output).replace("b'" + string_prefix, "").replace("'", "").replace("\\n", "")
    str_splitted = result.split(' : ')
    if len(str_splitted) > 1:
        return str_splitted[1]
    else:
        return ""


def get_file_modification_datetime(path):
    logger.info("ctime = {}, mtime = {}, atime = {}".format(
        datetime.fromtimestamp(time.mktime(time.localtime(os.path.getctime(path)))),
        datetime.fromtimestamp(time.mktime(time.localtime(os.path.getmtime(path)))),
        datetime.fromtimestamp(time.mktime(time.localtime(os.path.getatime(path))))))
    logger.info("Use file modification datetime...")
    return datetime.fromtimestamp(time.mktime(time.localtime(os.path.getmtime(path))))


def get_video_create_datetime(path):
    return get_file_modification_datetime(path)


def sort(inner_directory, output_directory, recursive):
    for filename in os.listdir(inner_directory):
        if not filename.startswith('.'):  # Ignore hidden files
            if os.path.isfile(os.path.join(inner_directory, filename)):
                with open(os.path.join(inner_directory, filename), 'rb') as file:
                    logger.info("Reading file {}...".format(os.path.join(inner_directory, filename)))

                    extension = Path(filename).suffix[1:]  # Remove trailing point between filename and extension

                    do_sorting = False

                    if extension.lower() in image_types:
                        access_time = get_image_create_datetime(os.path.join(inner_directory, filename))
                        do_sorting = True
                    elif extension.lower() in video_types:
                        access_time = get_video_create_datetime(os.path.join(inner_directory, filename))
                        do_sorting = True
                    else:
                        logger.error("Error: file extension unknown for file {}"
                                     .format(os.path.join(inner_directory, filename)))

                    if do_sorting:
                        # Make subdirectory like: filename/year/month/day
                        file_path = output_directory
                        for subdir_name in (access_time.year, month_name[access_time.month - 1], access_time.day):
                            file_path = os.path.join(file_path, str(subdir_name))
                            if not os.path.exists(file_path):
                                os.makedirs(file_path)

                        i = 0

                        new_filename = get_file_name(access_time, extension, i)

                        # Copy the image if does not already exists
                        while os.path.exists(os.path.join(file_path, new_filename)):
                            i = i + 1
                            new_filename = get_file_name(access_time, extension, i)

                        input_file, output_file = os.path.join(inner_directory, filename), os.path.join(
                            file_path,
                            new_filename)
                        logger.info("Copying {} to {}".format(input_file, output_file))
                        copy2(input_file, output_file)
            else:
                if recursive & (os.path.join(inner_directory, filename) != output_directory):
                    sort(os.path.join(inner_directory, filename), output_directory, recursive)


def batch_rename(inner_directory, output_directory, date):
    i = 0
    for filename in os.listdir(inner_directory):
        if not filename.startswith('.'):  # Ignore hidden files
            extension = Path(filename).suffix[1:]

            if os.path.isfile(os.path.join(inner_directory, filename)):
                new_filename = get_file_name(date, extension, i)

                while os.path.exists(os.path.join(output_directory, new_filename)):
                    i = i + 1
                    new_filename = get_file_name(date, extension, i)

                input_file, output_file = os.path.join(inner_directory, filename), os.path.join(
                    output_directory,
                    new_filename)
                logger.info("Copying {} to {}".format(input_file, output_file))
                copy2(input_file, output_file)


COUNT = 0


def update_timezone_metadata(inner_directory, timezone, timezone_sign):
    global COUNT

    for filename in os.listdir(inner_directory):
        if not filename.startswith('.'):
            if os.path.isfile(os.path.join(inner_directory, filename)):
                extension = Path(filename).suffix[1:]

                if extension.lower() in image_types:
                    cmd = 'exiftool "-timeZoneOffset=' + timezone_sign + timezone + '" -overwrite_original -m "' \
                          + os.path.join(inner_directory, filename) + '"'
                    os.system(cmd)

                    final_timezone = timezone_sign

                    if int(timezone) < 10:
                        final_timezone += "0"

                    final_timezone += timezone + ":00"
                    logger.info("Final timezone = {}".format(final_timezone))

                    cmd_2 = 'exiftool "-timeZone=' + final_timezone + '" -overwrite_original -m "' \
                            + os.path.join(inner_directory, filename) + '"'
                    os.system(cmd_2)

                    COUNT = COUNT+1
                else:
                    logger.info("File {} is not an image".format(filename))
            else:
                update_timezone_metadata(os.path.join(inner_directory, filename), timezone, timezone_sign)


def check_directories(input_directory, output_directory):
    if not os.path.exists(input_directory):
        raise NotADirectoryError('No directory at %s.', input_directory)
    if not os.path.exists(output_directory):
        logger.info("Missing output directory at %s. Creating it…", output_directory)
        os.makedirs(output_directory)


def shift_all_date(input_directory, shift_sign, shift_string):
    for filename in os.listdir(input_directory):
        if not filename.startswith('.'):
            if os.path.isfile(os.path.join(input_directory, filename)):
                extension = Path(filename).suffix[1:]

                if extension.lower() in image_types:

                    shift_cmd = 'exiftool "-AllDates' + shift_sign + '=' + shift_string + '" -overwrite_original -m "' \
                          + os.path.join(input_directory, filename) + '"'
                    os.system(shift_cmd)
                else:
                    logger.info("File {} is not an image".format(filename))
            else:
                shift_all_date(os.path.join(input_directory, filename), shift_sign, shift_string)


if __name__ == "__main__":
    choice = input("Do you want to sort (s), batch rename (r), change timezone metadata (t), shift all date (sd) or "
                   "overwrite metadata (o) ? ")

    if choice == "s":
        # print
        input_directory = input("Select input_directory: ")
        output_directory = input_directory + "new"
        recursive = True

        check_directories(input_directory, output_directory)
        sort(input_directory, output_directory, recursive)
    elif choice == "r":
        input_directory = input("Select directory to batch rename files: ")
        output_directory = input_directory + "new"
        date = datetime.fromisoformat(input("Select date to rename file (YYYY-MM-DDTHH:MM:SS): "))

        check_directories(input_directory, output_directory)
        batch_rename(input_directory, output_directory, date)

    elif choice == "t":
        input_directory = input("Select directory of your files you want to change timezone metadata: ")
        timezone = input("Enter your timezone value (eg: 4): ")
        timezone_sign = input("Enter your timezone sign (eg: -/+): ")
        update_timezone_metadata(input_directory, timezone, timezone_sign)
        logger.info("Nb image updated = {}".format(COUNT))

    elif choice == "sd":
        input_directory = input("Select directory of your files you want to shift time metadata: ")
        shift_sign = input("Add (+) or remove (-) time:")
        shift_string = input("Enter the shift string (eg: Y:MM:DD TT:MM:SS): ")
        shift_all_date(input_directory, shift_sign, shift_string)

    elif choice == "o":
        print("\nOpen a new terminal and type: \n\t\texiftool -j my_image.jpg >> my_image.json")
        print("Then to overwrite tags from json file, type this command: \n\t\texiftool -j+=my_source_json.json "
              "image_to_overwrite.jpg")

    logger.info("")
    logger.info("----------------------------------------------------------------------------")
    logger.info("----------------------               END             -----------------------")
    logger.info("----------------------------------------------------------------------------")
