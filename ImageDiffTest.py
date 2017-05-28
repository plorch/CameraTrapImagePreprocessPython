import os
from os.path import splitext
import csv
import sys
from PIL import Image, ImageChops
import math
import numpy as np
import time

# This is from
# http://stackoverflow.com/questions/5524179/how-to-detect-motion-between-two-pil-images-wxpython-webcam-integration-exampl
#  Answer 1 using modified entropy calculation

# Check first if the given path exists before continuing to the next step.
#  Path can be cut and pasted from windows file explorer or whatever

#while True:
#    folderpath = raw_input('Folder path: ')
#    print "\nChecking if folder path exists...\n"
#    if os.path.exists(folderpath):
#        print "Ok!\n"
#        break;
#    else:
#        print "%s does not exist. Please enter a valid path.\n" % folderpath

# For testing uncomment this
folderpath= 'C:\\Users\\pdl\\Desktop\\test'


dirname = os.path.basename(folderpath)
print "Directory name %s\n" % dirname

def image_entropy(img):
    w,h = img.size
    a = np.array(img.convert('RGB')).reshape((w*h,3))
    h,e = np.histogramdd(a, bins=(16,)*3, range=((0,256),)*3)
    prob = h/np.sum(h) # normalize
    prob = prob[prob>0] # remove zeros
    return -np.sum(prob*np.log2(prob))

def get_filenames(fpath=folderpath): #
    os.chdir(fpath)
    files=os.listdir('.')
    return [i for i in files if splitext(i)[1].lower() in {'.jpg', '.png', '.JPG', '.PNG'}]

if __name__ == '__main__':
    t = time.clock()
    filenames = get_filenames()

#    if not os.path.exists('diffs'):
#        os.makedirs('diffs')
        
    for i in xrange(len(filenames)):
        num = i + 1
        digits = len(str(num))
        current_file = filenames[i]

# Make entropies and save diffs
    with open("entropies.csv",'wb') as f:  #diffs\\
        w=csv.writer(f)
        # To write the first row
        w.writerow(['Image 1','Image 2','Image 3','ID', '#Entropy12', '#Entropy23','#Entropy13'])
        ID=1
        tt = time.clock()
        print tt-t
        for i in xrange(0,len(filenames),3):
            img1 = Image.open(filenames[i])
            img2 = Image.open(filenames[i+1])
            img3 = Image.open(filenames[i+2])
#            print os.path.splitext(filenames[i])[0]
            img12 = ImageChops.difference(img1,img2)
            newpath="%s_diff_%s.jpg" % (os.path.splitext(filenames[i])[0],os.path.splitext(filenames[i+1])[0]) #diffs\\
            img12.save(newpath)
            entropy12=image_entropy(img12)
            img23 = ImageChops.difference(img2,img3)
            newpath="%s_diff_%s.jpg" % (os.path.splitext(filenames[i+1])[0],os.path.splitext(filenames[i+2])[0]) #diffs\\
            img23.save(newpath)
            entropy23=image_entropy(img23)
            img13 = ImageChops.difference(img1,img3)
            newpath="%s_diff_%s.jpg" % (os.path.splitext(filenames[i+2])[0],os.path.splitext(filenames[i])[0]) #diffs\\
            img13.save(newpath)
            entropy13=image_entropy(img13)
    
            w.writerow([filenames[i],filenames[i+1],filenames[i+2],ID,entropy12,entropy23,entropy13])
            ID=ID+1

    ttt = time.clock()
    print ttt-tt
    