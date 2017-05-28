from PIL import Image, ImageChops
import os
# import math
# import numpy as np

def image_reduce(img,redfac=2):
    w,h = img.size
    size=(int(round(w/redfac)),int(round(h/redfac)))
#   redfac=2 or 50% reduction should give (960,720) which is still big enough to view
    img=img.resize(size,Image.ANTIALIAS)
    return (img)
    
# For now we assume this is running in the directory you have a subset of images
#  in.  Should be 999 or fewer for Zooniverse.   
#  Once this works, change to opperate on all dirs in the current folder (see *** below).
#  Once that works, specify the directory to go to to do the job.
files = [ f for f in os.listdir('.') if f[-4:].lower() in ('.jpg','.png') ]
# Use something like this if you want to traverse dirs
# Source: http://stackoverflow.com/questions/2632205/how-to-count-the-number-of-files-in-a-directory-using-python
# replacing '.' with DIR and use something like 'if os.path.isfile(os.path.join(DIR, name))'
# files = [ f for f in os.listdir('.') if f[-4:].lower() in ('.jpg','.png') ]

# Need to rename images with exif data before resizing, since resizing losses exif data

# *** Rename current folder to RRNNNN__Date and subfolders to RRNNNN__Date_1...
#  Use these folder names to rename files inside them.
if not os.path.exists('toupload'):
    os.makedirs('toupload')
    
for (index,filename) in enumerate(files):
    img1 = Image.open(filename)
    img2=image_reduce(img1)
    newpath="toupload\\%s" % filename
    img2.save(newpath,optimize=True,quality=95)


#    print os.stat('somefile.ext').st_size
