#!C:/Python27/python.exe
# Needs to be run in Python 2.X and this shebang does not seem to work
# So use `py -2 path`
# py -2 .\FindAndTagEmptyImages.py 'E:\UNPROCESSED\6th_checkJune2016_tagged_good'

import re
import sys
import os
import datetime
import time
from PIL import Image
from PIL.ExifTags import TAGS
import numpy as np
import pandas as pd

""" Construct a panda with current filenames and paths, create datetime, and tags."""


# Number of seconds to use when identifying empty images from unmarked
SKIP = 180


def get_image_paths(folderpath):
    """Get image paths."""
    return (os.path.join(folderpath, f)
      for f in os.listdir(folderpath)
      if os.path.splitext(f)[1].lower() in {'.jpg', '.png'})


def get_exif_data_img(filename,img):
    """Get embedded EXIF data from image file."""

    # Source: <a href="http://www.endlesslycurious.com/2011/05/11/extracting-image-exif-data-with-python/">http://www.endlesslycurious.com/2011/05/11/extract...</a>

    ret = {}
    try:
        if hasattr(img, '_getexif'):
            exifinfo = img._getexif()
            if exifinfo is not None:
                for tag, value in exifinfo.items():
                    decoded = TAGS.get(tag, tag)
                    if decoded == 'DateTimeOriginal':
# There are multiple possible date formats.  Find out what is needed first
#   '%Y-%m-%dT%H:%M:%S', '%Y:%m:%d %H:%M:%S'
                        ret = datetime.datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                        break
                    else:
                        ret = None
    except IOError:
        print('IOERROR ' + filename)
#    img.close()
    return ret


def get_exif_xmp_data(filename):
    """Get embedded EXIF data from image file XMP."""
# Source: http://www.endlesslycurious.com/2011/05/11/extracting-image-exif-data-with-python/
#   and https://stackoverflow.com/questions/6822693/read-image-xmp-data-in-python?noredirect=1&lq=1

# This turns out to be easy for the DateTimeOriginal, since it is stored in
#   regular exif.  Subject tags are stored in xmp and are harder to pull out.
#   Rather than get date using _getexif, I just get it from the XMP too when
#   I can (digiKam scored, not windows media player).
#   EXIF and particularly XMP exif are highly irregular so this program is
#   fragile.

    try:
        img = Image.open(filename)
        if hasattr(img, 'applist'):
# reversed() below allows gets to APP1 and http://... first, avoiding assigning
#   subject twice. Will work if order of 2 APP1 segments are reversed.
            for segment, content in reversed(img.applist):
                # print("segment: %s " % segment)
                marker, body = content.split('\x00', 1)
                # print("marker: %s\n" % marker)
                # print("File: %s, Segment: %s, marker: %s " % (os.path.basename(filename), segment, marker))
                if segment == 'APP1':
                    if (marker == 'http://ns.adobe.com/xap/1.0/'): #  | marker[1:] == b'http://ns.adobe.com/xap/1.0/'
                        bd = body[body.find('<dc:subject>'):body.find('</dc:subject>')]
# This is to account for ones where there is XMP data but no subject tags
                        if bd is not '':
                            subject = bd[bd.find('<rdf:li>')+8:bd.find('</rdf:li>')]
                        else:
                            subject = 'untagged'
# This is crude, but seems like fastest way to grab date from xmp dictobj
#   like this exif:DateTimeOriginal="2015-12-08T12:19:04" without making it a
#   dictobj, since we don't need any other items.
                        DateTimeOriginal = get_exif_data_img(filename, img)
                        break
                    else:
                        subject = 'untagged'
                        DateTimeOriginal = get_exif_data_img(filename, img)

    except IOError:
        print('IOERROR ' + filename + ' is bad')
#    img.close()
    return subject, DateTimeOriginal


def purge(dir, pattern):
    """ Remove extraneous files created by windows, mac OS, or iOS."""
    for f in os.listdir(dir):
        if re.match(pattern, f):
            os.remove(os.path.join(dir, f))


if __name__ == '__main__':
    folderpath = sys.argv[-1]
    print("\nChecking if folder path exists...\n")
    if os.path.exists(folderpath):
        print("Ok!\n")
    else:
        print("%s does not exist.\n" % folderpath)
        sys.exit("Bad path!")
    check = os.path.split(folderpath)[1]
    print("Check name: %s\n" % check)

# For now we are assuming no subfolders under camera folder, which is how Rem
#   has been sending them. If this becomes untrue, look at how its done in
#  image_file_crunch_Parall4.py


# This version should go through this loop once for each camera so dirpath will
#   end with camera card name.
    cams = os.listdir(folderpath)
    # This avoids walking check directories, looking for images
    t = time.clock()
    i = 0
    for cam in cams:
        t1 = time.clock()
        campath = os.path.join(folderpath, cam)
        camname = cam
        print("Camera card name: %s\n" % camname)
# Remove hidden files starting with ._ created by viewing cards on iPads or mac
        purge(campath, "\._")
# Get filepaths for files in dir that end in .jpg or .png
        filepaths = get_image_paths(campath)
        rows_list = []
        for path in filepaths:
            filename, file_extension = os.path.splitext(path)
            if file_extension.lower == '.png':
                print("Encountered a .png, skipping")
                continue
            subj, datetimeoriginal = get_exif_xmp_data(path)
            dict1 = {'path': path,
                     'filename': os.path.split(path)[1],
                     'datetimeoriginal': pd.Timestamp(datetimeoriginal),
                     'subject': subj}
            rows_list.append(dict1)
        df = pd.DataFrame(rows_list)
# May want to comment this line out when printing manifests for each camera
        df['camera'] = camname
        df['diff_sec'] = df['datetimeoriginal'].diff().astype('timedelta64[s]')
        df['subject2'] = np.where(df['subject'] != 'untagged', df['subject'],
                                  np.where(df['diff_sec'] > SKIP, 'empty', ''))
# Comment out if you don't need to eliminate head and tail images with
#   camera case
        # df['cum_secs'] = df.diff_sec.cumsum()
        df_filename = os.path.join(campath, 'manifest_w_empty.csv')
# To not make one manifest for each camera, toggle comment on the line below
        # df.to_csv(df_filename, mode='w', index=False)
# Debug code, can be commented out
        t2 = time.clock()
        print("Processed manifest for %s in %s min\n" % (camname, ((t2-t1)/60)))
# To make one manifest for whole check, toggle the comments on 2 lines below
        df_checkname = os.path.join(folderpath, 'manifest_w_empty.csv')
        df.to_csv(df_checkname, mode='a', index=False,
                  header=(True if i == 0 else False))
        i += 1
    tt = time.clock()
    print("Exported manifest for %s in %s min" % (check, ((tt-t)/60)))
