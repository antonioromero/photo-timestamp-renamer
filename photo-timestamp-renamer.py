from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
import time
import os
import imghdr
import sys


def get_exif_tag(file,  tag):
    
    img = Image.open(file)
    if hasattr(img, '_getexif'):
        exif_data = img._getexif()
        exif_data.items()
        if exif_data is not None:
            for key,  value in exif_data.items():
                if TAGS.get(key) == tag:
                    date_time = value
            return date_time
        else:
            print('Error en: ' + file)


def rename_file_to_timestamp(file):
    date_time = get_exif_tag(file,  'DateTime')
    if date_time is not None:
        date = datetime.strptime(date_time, "%Y:%m:%d %H:%M:%S")
        timestamp = time.mktime(date.timetuple())

        path,  original_name = os.path.split(file)
        file_name,  file_extension = os.path.splitext(original_name)
        new_name = path + os.sep + str(int(timestamp)) + file_extension
        os.rename(file,  new_name)


def go_over_directory(action,  path):
    for file in os.listdir(path):
        image = path + os.sep + file
        try:
            Image.open(image)
            if imghdr.what(image) == 'jpeg':
                action(image)
        except IOError:
            print(sys.exc_info())

go_over_directory(rename_file_to_timestamp, sys.argv[1])