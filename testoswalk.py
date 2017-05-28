import os
rootdir = r'P:\WildlifeCameraStudyImages\4th Check April 2016\BC1122b'
# Swap this in to process one camera \BC1122b
# So all you have to do is change to a higher directory to do all cameras
for subdir, dirs, files in os.walk(rootdir):
    #for file in files:
    #    print os.path.join(subdir, file)
#    print subdir
    for dir in dirs:
        print os.path.join(subdir, dir)