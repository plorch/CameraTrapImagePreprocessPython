import re
import os
import csv
import sys
import shutil
import math
import datetime
import time
from PIL import Image, ImageChops, ImageDraw
from PIL.ExifTags import TAGS
from multiprocessing import Pool

""" Rename files based on current folder name, Date and Time from exif data
  Files are resized to below Zooniverse's threshold of 600Kb, the camera name is
  obscured, and we write out a manifest for Zooniverse upload.
This version uses filepath rather than name for the multiprocessed part. It works
with camera directory as input.  This must be pasted into a global variable below
becuase you cannot pass things that come from STDIN to another process.
This one also does all cameras in a camera check.

Creates a manifest and toupload folder for each camera subdirectory.

Need to:
  create toupload in correct place
  put reduced obscured images in that folder
  write manifest for that folder

 Source for rename: https://www.calazan.com/python-script-for-auto-renaming-your-image-files/
 and
 http://chriskiehl.com/article/parallelism-in-one-line/
"""
    
# Uncomment this if you want user control over filename and comment next line
# filename_pattern = raw_input('Filename pattern: ')
# Uncomment if you don't want user control
filename_pattern = '<ck>_<cname>_<dname>__<datetaken>__<num>.jpg'
SAVE_DIRECTORY='toupload'
# The r below turns the string into a raw string, preventing the \ from causing escapes
folderpath = r"E:\UNPROCESSED\8th check August 2016\8thCheckAugust2016_2readytoupload"

def get_exif_data(filename):
    """Get embedded EXIF data from image file.

    Source: <a href="http://www.endlesslycurious.com/2011/05/11/extracting-image-exif-data-with-python/">http://www.endlesslycurious.com/2011/05/11/extract...</a>
    """
    ret = {}
    try:
        img = Image.open(filename)
        if hasattr( img, '_getexif' ):
            exifinfo = img._getexif()
            if exifinfo != None:
                for tag, value in exifinfo.items():
                    decoded = TAGS.get(tag, tag)
                    ret[decoded] = value
    except IOError:
        print 'IOERROR ' + filename
#    img.close()
    return ret

def get_date_taken(filename):
    datestring = get_exif_data(filename)['DateTimeOriginal']
    return datetime.datetime.strptime(datestring, '%Y:%m:%d %H:%M:%S')

def get_filenames(folderpath): #
    os.chdir(folderpath)
    files=os.listdir('.')
    return [i for i in files if os.path.splitext(i)[1].lower() in {'.jpg', '.png'}]

def get_image_paths(folderpath):
  return (os.path.join(folderpath, f) 
      for f in os.listdir(folderpath) 
      if os.path.splitext(f)[1].lower() in {'.jpg', '.png'})

def get_numbering_format(digits, num):
    if digits == 1:
        numberfmt = '0000%s' % num
    elif digits == 2:
        numberfmt = '000%s' % num
    elif digits == 3:
        numberfmt = '00%s' % num
    elif digits == 4:
        numberfmt = '0%s' % num
    else:
        numberfmt = '%s' % num
    return numberfmt

def date_to_string(dateobj, format):
    return datetime.datetime.strftime(dateobj, format)

def multi_replace(text, dictobj):
    """Replace characters in the text based on the given dictionary."""
    for k, v in dictobj.iteritems():
        text = text.replace(k, v)
    return text

def image_reduce(img,redfac=2):
    w,h = img.size
    size=(int(round(w/redfac)),int(round(h/redfac)))
#   redfac=2 or 50% reduction should give (960,720) which is still big enough to view
    img=img.resize(size,Image.ANTIALIAS)
    return (img)
    
def fileRename(current_file,num,digits):
    """Replace old filename with one based on camera name (dir name) and date/time."""
    # Key, value pairs of what to replace.
    dictobj = {
        '<num>': get_numbering_format(digits, num),
        '<datetaken>': date_to_string(get_date_taken(current_file),'%Y%m%d__%H_%M'),
        '<dname>': dirname,
        '<cname>': camname,
        '<ck>': check
    }
    # Rename
    new_filename = os.path.join(os.path.dirname(current_file),multi_replace(filename_pattern, dictobj))
    shutil.move(current_file, new_filename)
    return(new_filename)

def fileResizeObscure(new_filename):
    """Resize file and obscure camera name.  Saving this file removes the GPS coordinates."""
    # Resize
    img1 = Image.open(new_filename)
    img2=image_reduce(img1)
#    img1.close()
    newpath=os.path.join(os.path.split(os.path.dirname(new_filename))[0],SAVE_DIRECTORY,os.path.split(new_filename)[1])
    # Block ID
    width=img2.size[0]
    height=img2.size[1]
    #  Obscuring params were decided by trial and error using fraction of width and height
    x1=int(0.16*width)
    x2=int(0.28*width)
    y1=int(0.94*height)
    y2=int(0.98*height)         
    #  Faster but easier to snoop? should not be since it changes the pixels
    draw = ImageDraw.Draw(img2)
    draw.rectangle([(x1,y1),(x2,y2)],fill="white")
    del draw
    
    img2.save(newpath,optimize=True,quality=95)

def purge(dir, pattern):
    for f in os.listdir(dir):
    	if re.match(pattern, f):
    	   os.remove(os.path.join(dir, f))

if __name__ == '__main__':
# Check first if the given path exists before continuing to the next step.
    print "\nChecking if folder path exists...\n"
    if os.path.exists(folderpath):
        print "Ok!\n"
    else:
        print "%s does not exist.\n" % folderpath
        sys.exit("Bad path!")
    check=os.path.split(folderpath)[1]
    print "Check name: %s\n" % check
    
# This version should go through this loop once for each camera so dirpath will
#   end with camera card name.
    cams=os.listdir(folderpath)
    # This avoids walking check directories, looking for images
    for cam in cams:
        campath=os.path.join(folderpath,cam)
        for dirpath, dirs, files in os.walk(campath):
            ncamdirs=0
            t1=t= time.clock()
            camname=os.path.split(dirpath)[1]
            print "Camera card name: %s\n" % camname
            i=0
            # Once for each subdir in a camera dir
            for dir in dirs:
                print "Current directory path: %s\n" % os.path.join(dirpath,dir)
                # Remove hidden files starting with ._ created by viewing cards on iPads
                dirname = dir
                purge(os.path.join(dirpath,dir),"\._")
                # Get filepaths for files in dir that end in .jpg or .png
                filepaths=get_image_paths(os.path.join(dirpath,dir))
                for path in filepaths:
                    i = i + 1
                    digits = len(str(i))
            
                    # Only rename, resize and block ID files, ignore directories.
                    if not os.path.isdir(path):
                        # Rename files using filename_pattern but not directories
                        new_filename=fileRename(path,i,digits)
            
                tt = time.clock()
                print "Rename: %s minutes" % ((tt-t)/60)
    
                # After renaming get filepaths again        
                newfilepaths=get_image_paths(os.path.join(dirpath,dir))
                #print "\n".join(newfilepaths)
    
    # Use of dirpath here means their is only one "toupload" folder created per camera
                if not os.path.exists(os.path.join(dirpath,SAVE_DIRECTORY)):
                    os.makedirs(os.path.join(dirpath,SAVE_DIRECTORY))
                
                tt = time.clock()
                pool=Pool()
                pool.map(fileResizeObscure,newfilepaths)
                pool.close()
                pool.join()
                        
            # Make manifest
                fpath=os.path.join(dirpath,SAVE_DIRECTORY)
                with open(os.path.join(fpath,"manifest.csv"),'wb') as f:
                    filenames=get_filenames(fpath)
                    w=csv.writer(f)
                    # To write the first row
                    # w.writerow(['Image 1','Image 2','Image 3','ID'])
    #  Next line removes data on camera name from appearing when you click i button by adding #
                    w.writerow(['#Image 1','#Image 2','#Image 3','ID'])
                    ID=1
                    tt = time.clock()
                    print "Resize, and obscure: %s minutes" % ((tt-t)/60)
                    for i in xrange(0,len(filenames),3):
                        w.writerow([filenames[i],filenames[i+1],filenames[i+2],ID])
                        ID=ID+1
                
                f.close()
                ttt = time.clock()
            
                print "Manifest: %s minutes\n" % ((ttt-tt)/60)
                t=time.clock()
                tt=time.clock()
    
            ncamdirs=ncamdirs+1
    
    print "\nTotal time for %s subfolders is %s minutes\n" % ((ncamdirs-1),((time.clock()-t1)/60))
