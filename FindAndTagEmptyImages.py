import re
import sys
import os
import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import numpy as np
import pandas as pd

""" Construct a panda with current filenames and paths, create datetime, and tags."""

# x 1. get info from args
# x 2. get file list
#   a. starting with just one camera directory with no subdirs
# x 3. get datetime and TAGS
# 4. figure out empties and tag files


def get_image_paths(folderpath):
    """Get image paths."""
    return (os.path.join(folderpath, f)
      for f in os.listdir(folderpath)
      if os.path.splitext(f)[1].lower() in {'.jpg', '.png'})


def get_exif_xmp_data(filename):
    """Get embedded EXIF data from image file XMP."""
# Source: <a href="http://www.endlesslycurious.com/2011/05/11/extracting-image-exif-data-with-python/">http://www.endlesslycurious.com/2011/05/11/extract...</a>
#   and https://stackoverflow.com/questions/6822693/read-image-xmp-data-in-python?noredirect=1&lq=1

# This turns out to be easy for the DateTimeOriginal, since it is stored in
#   regular exif.  Subject tags are stored in xmp and are harder to pull out.
#   Rather than get date using _getexif, I just get it from the XMP too. EXIF
#   and particularly XMP exif are highly irregular so this program is fragile.

    try:
        img = Image.open(filename)
        if hasattr(img, 'applist'):
# reversed() below allows gets to APP1 and http://... first, avoiding assigning
#   subject twice. Will work if order of 2 APP1 segments are reversed.
            for segment, content in reversed(img.applist):
                marker, body = content.split('\x00', 1)
                # print "File: %s, Segment: %s, marker: %s " % (os.path.basename(filename), segment, marker)
                if segment == 'APP1':
                    if marker == 'http://ns.adobe.com/xap/1.0/':
                        bd = body[body.find('<dc:subject>'):body.find('</dc:subject>')]
# This is to account for ones where there is XMP data but no subject tags
                        if bd is not '':
                            subject = bd[bd.find('<rdf:li>')+8:bd.find('</rdf:li>')]
                        else:
                            subject = 'untagged'
# This is crude, but seems like fastest way to grab date from xmp dictobj
#   like this exif:DateTimeOriginal="2015-12-08T12:19:04" without making it a
#   dictobj, since we don't need any other items.
                        datestring = body[body.find('exif:DateTimeOriginal')+23:body.find('exif:DateTimeOriginal=')+42]
                        DateTimeOriginal = datetime.datetime.strptime(datestring, '%Y-%m-%dT%H:%M:%S')
                        break
                    else:
                        subject = 'untagged'
                        exifinfo = img._getexif()
                        if exifinfo is not None:
                            for tag, value in exifinfo.items():
                                decoded = TAGS.get(tag, tag)
                                if decoded == 'DateTimeOriginal':
                                    DateTimeOriginal = datetime.datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                                    break
                                else:
                                    DateTimeOriginal = None
                        # break

    except IOError:
        print 'IOERROR ' + filename
#    img.close()
    return subject, DateTimeOriginal


def purge(dir, pattern):
    """ Remove extraneous files created by mac OS."""
    for f in os.listdir(dir):
        if re.match(pattern, f):
            os.remove(os.path.join(dir, f))


if __name__ == '__main__':
    folderpath = sys.argv[-1]
    print "\nChecking if folder path exists...\n"
    if os.path.exists(folderpath):
        print "Ok!\n"
    else:
        print "%s does not exist.\n" % folderpath
        sys.exit("Bad path!")
    check = os.path.split(folderpath)[1]
    print "Check name: %s\n" % check

# For now we are assuming no subfolders under camera folder, which is how Rem
#   has been sending them. If this becomes untrue, look at how its done in
#  image_file_crunch_Parall4.py


# This version should go through this loop once for each camera so dirpath will
#   end with camera card name.
    cams = os.listdir(folderpath)
    # This avoids walking check directories, looking for images
    for cam in cams:
        campath = os.path.join(folderpath, cam)
        camname = cam
        print "Camera card name: %s\n" % camname
# Remove hidden files starting with ._ created by viewing cards on iPads
        purge(campath, "\._")
# Get filepaths for files in dir that end in .jpg or .png
        filepaths = get_image_paths(campath)
        rows_list = []
        for path in filepaths:
            subj, datetimeoriginal = get_exif_xmp_data(path)
            dict1 = {'path': path,
                     'filename': os.path.split(path)[1],
                     'datetimeoriginal': pd.Timestamp(datetimeoriginal),
                     'subject': subj}
            rows_list.append(dict1)
# For now we are exporting manifest for each dir
        df = pd.DataFrame(rows_list)
        df['diff_sec'] = df['datetimeoriginal'].diff().astype('timedelta64[s]')
        df['subject2'] = np.where(df['subject'] != 'untagged', df['subject'],
                                  np.where(df['diff_sec'] > 180, 'empty', ''))
# Export to .csv
        df_filename = os.path.join(campath, 'manifest_w_empty.csv')
        df.to_csv(df_filename, mode='a', index=False)
        print "Done exporting manifest for %s" % campath
