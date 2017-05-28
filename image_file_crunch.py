import os
from os.path import splitext
import csv
import sys
import shutil
import math
import numpy as np
import datetime
import time
from PIL import Image, ImageChops, ImageDraw
from PIL.ExifTags import TAGS

""" Rename files based on current folder name, Date and Time from exif data
  Files are resized to below Zooniverse's threshold of 600Kb, the camera name is
  obscured, and we write out a manifest for Zooniverse upload. This version 
  calculates entropy across whole images.  This does not help distinguish false
  triggers, so it was removed.

 Source for rename: https://www.calazan.com/python-script-for-auto-renaming-your-image-files/
"""

# Need to mod this to only consecutively number within 
# one minute?
    
# Check first if the given path exists before continuing to the next step.
#  Path can be cut and pasted from windows file explorer or whatever
while True:
    folderpath = raw_input('Folder path: ')
    print "\nChecking if folder path exists...\n"
    if os.path.exists(folderpath):
        print "Ok!\n"
        break;
    else:
        print "%s does not exist. Please enter a valid path.\n" % folderpath

dirname = os.path.basename(folderpath)
print "Directory name %s\n" % dirname

# Uncomment this if you want user control over filename and comment next line
# filename_pattern = raw_input('Filename pattern: ')
# Uncomment if you don't want user control
filename_pattern = '<dname>__<datetaken>__<num>.jpg'

def get_exif_data(filename):
    """Get embedded EXIF data from image file.

    Source: <a href="http://www.endlesslycurious.com/2011/05/11/extracting-image-">http://www.endlesslycurious.com/2011/05/11/extract...</a>             exif-data-with-python/
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
    return ret

def get_date_taken(filename):
    datestring = get_exif_data(current_file)['DateTimeOriginal']
    return datetime.datetime.strptime(datestring, '%Y:%m:%d %H:%M:%S')

def get_filenames(fpath=folderpath): #
    os.chdir(fpath)
    files=os.listdir('.')
    return [i for i in files if os.path.splitext(i)[1].lower() in {'.jpg', '.png', '.JPG', '.PNG'}]

def get_image_paths(fpath=folderpath):
  return (os.path.join(fpath, f) 
      for f in os.listdir(fpath) 
      if 'jpeg' in f)

def get_numbering_format(digits, num):
    if digits == 1:
        numberfmt = '00%s' % num
    elif digits == 2:
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

"""  This is from
 http://stackoverflow.com/questions/5524179/how-to-detect-motion-between-two-pil-images-wxpython-webcam-integration-exampl
  Answer 1 using modified entropy calculation
"""
def image_entropy(img):
    w,h = img.size
    a = np.array(img.convert('RGB')).reshape((w*h,3))
    h,e = np.histogramdd(a, bins=(16,)*3, range=((0,256),)*3)
    prob = h/np.sum(h) # normalize
    prob = prob[prob>0] # remove zeros
    return -np.sum(prob*np.log2(prob))
    
""" This is from
http://stackoverflow.com/questions/3002085/python-to-print-out-status-bar-and-percentage
answer 6
"""
def drawProgressBar(percent, barLen = 20):
    sys.stdout.write("\r")
    progress = ""
    for i in range(barLen):
        if i < int(barLen * percent):
            progress += "="
        else:
            progress += " "
    sys.stdout.write("[ %s ] %.2f%%" % (progress, percent * 100))
    sys.stdout.flush()

def fileRename(current_file,num,digits):
    """Replace old filename with one based on camera name (dir name) and date/time."""
    # Key, value pairs of what to replace.
    dictobj = {
        '<num>': get_numbering_format(digits, num),
        '<datetaken>': date_to_string(get_date_taken(current_file),'%Y%m%d__%H_%M'),
        '<dname>': dirname
    }
    # Rename
    new_filename = multi_replace(filename_pattern, dictobj)
    shutil.move(current_file, new_filename)
    return(new_filename)

def fileResizeObscure(new_filename):
    """Resize file and obscure camera name.  Saving this file removes the GPS coordinates."""
    # Resize
    img1 = Image.open(new_filename)
    img2=image_reduce(img1)
    newpath="toupload\\%s" % new_filename
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

if __name__ == '__main__':
    t = time.clock()
    filenames = get_filenames()
    filecount = len(filenames)
    print "%s files to process\n" % filecount
    print "%s file sets\n" % (filecount/3)

    if not os.path.exists('toupload'):
        os.makedirs('toupload')
        
    for i in xrange(filecount):
        num = i + 1
        digits = len(str(num))
        current_file = filenames[i]

        # Only rename, resize and block ID files, ignore directories.
        if not os.path.isdir(current_file):
            # Rename files using filename_pattern but not directories
            new_filename=fileRename(current_file,num,digits)

            # Resize
            fileResizeObscure(new_filename)
            
# This is not working and needs debugging.           
#            drawProgressBar((i/filecount), barLen = 20)
            

# Make manifest
    with open("toupload\\manifest.csv",'wb') as f:
        filenames=get_filenames(fpath='toupload')
        w=csv.writer(f)
        # To write the first row
#        w.writerow(['Image 1','Image 2','Image 3','ID', '#Entropy12', '#Entropy23'])
#  Next line is an attempt to remove data on camera name from appearing when you click i button
        w.writerow(['#Image 1','#Image 2','#Image 3','ID', '#Entropy12', '#Entropy23'])
        ID=1
        tt = time.clock()
        print "Rename, resize, and obscure: %s minutes" % ((tt-t)/60)
        for i in xrange(0,len(filenames),3):
            img1 = Image.open(filenames[i])
            img2 = Image.open(filenames[i+1])
            img3 = Image.open(filenames[i+2])

            img12 = ImageChops.difference(img1,img2)
#            img12.save('test_diff832_833.jpg') # needs sensible name
            entropy12=image_entropy(img12)
            img23 = ImageChops.difference(img2,img3)
#            img23.save('test_diff832_833.jpg') # needs sensible name
            entropy23=image_entropy(img23)
            w.writerow([filenames[i],filenames[i+1],filenames[i+2],ID,entropy12,entropy23])
            ID=ID+1
            
    ttt = time.clock()
   
    print "Manifest and entropy: %s minutes" % ((ttt-tt)/60)