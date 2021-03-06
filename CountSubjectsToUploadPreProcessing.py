import os
import sys
import csv

""" Walk through dirs in subs of main dir and count total files in each sub-sub
    dir. For example if maindir is a whole check like 8thCheckAugust2016, the 
    subs would be camera folders with one or more subfolders in them.  We want 
    a file count of each sub-sub, summed over each sub (camera). File count 
    divided by 3 should give subjects (without decimal part, in case their are
    more than mod 3 files.
    
    Output should be camera folder name, count.
    
"""

folderpath = r"P:\WildlifeCameraStudyImages\8thCheckAugust2016"

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
    check_total=0
    # This avoid walking check directories, looking for images. Assumes all files
    # are image files.
    for cam in cams:
        cam_total=0
        campath=os.path.join(folderpath,cam)
        for dirpath, dirs, files in os.walk(campath):
            file_count = len(files)
            cam_total += file_count
#        print "%s has %d subjects" % (cam,cam_total/3)
        check_total += cam_total
    print "Check has %d subjects" % (check_total/3)
