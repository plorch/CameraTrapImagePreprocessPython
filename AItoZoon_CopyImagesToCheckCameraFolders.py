import pandas as pd
import sys
import os
# import shutil
import datetime
import time
# from threading import Thread

""" Take manifest from AI showing tagged files and copy them into folders by
check and camera in a way that makes sense for future Zoonivers uploads."""

# Calling this program will look like this:
# py -2 .\AItoZoon_CopyImagesToCheckCameraFolders.py 'C22' 'E:\UNPROCESSED\
# 22ndCheckJanuary2018\train_1000_2nd_4_server_weights_predictionsC22_BC.csv'

filename_pattern = '<ck>_<cname>_<datetaken>_<num>.jpg'
source_path = r'E:\UNPROCESSED\22ndCheckJanuary2018'
zoon_folder = 'zoon_upload'


def date_to_string(dateobj, format):
    """ Convert to string from datetime."""
    return datetime.datetime.strftime(dateobj, format)


def multi_replace(text, dictobj):
    """Replace characters in the text based on the given dictionary."""
    for k, v in dictobj.iteritems():
        text = text.replace(k, v)
    return text


def fileNewname(ck, camname, datetime, num):
    """Replace old filename with one based on check, camera name and date/time."""
    # Key, value pairs of what to replace.
    dictobj = {
        '<num>': str(num),
        '<datetaken>': datetime,
        '<cname>': camname,
        '<ck>': ck
    }
    # Rename
    new_filename = multi_replace(filename_pattern, dictobj)
    return(new_filename)


if __name__ == '__main__':
    manifest = sys.argv[-1]
# Check for bad paths
    print("\nChecking if file paths exists...\n")
    if os.path.exists(manifest):
        print("Input path Ok!\n")
    else:
        print("%s does not exist.\n" % manifest)
        sys.exit("Bad input path!")
    if os.path.exists(source_path):
        print("Output path Ok!\n")
    else:
        print("%s does not exist.\n" % source_path)
        sys.exit("Bad output path!")

    check = os.path.basename(os.path.split(manifest)[0])
    print("Check name: %s\n" % check)

    out_dir = os.path.join(source_path, zoon_folder)
    try:
        os.makedirs(out_dir)
    except OSError:
        if not os.path.isdir(out_dir):
            raise
    checkname = sys.argv[1]
# Read data into a panda
    df = pd.read_csv(manifest)
# Remove rows with no tag
    df = df[df.predicted.notna()]
# Add places to track source and dest file paths
# tep.apply(lambda x: os.path.join(r'E:/stuff',x))
    end_part = df.file_name.str.split('/', 1, expand=True)[1]
    df['sourcepath'] = end_part.apply(lambda x: os.path.abspath(os.path.join(source_path, x)))
    df['destpath'] = end_part.apply(lambda x: os.path.abspath(os.path.join(out_dir, x)))
    # df['sourcepath'] = ""
    # df['destpath'] = ""

# Create directories for image copies, if they don't exist
    # for subj in df.predicted.unique():
    #     subj_dir = os.path.join(out_dir, subj)
    #     try:
    #         os.makedirs(subj_dir)
    #     except OSError:
    #         if not os.path.isdir(subj_dir):
    #             raise

    t = time.clock()
# Do the copying using threading
    # i = 1
    # for index, row in df.iterrows():
        # subj2 = row['predicted']
        # src = row['path']
        # newfilename = fileNewname(checkname, row['camera'],
        #                           date_to_string(row['datetimeoriginal'],
        #                           '%Y%m%d__%H_%M_%S'), i)
        # df.sourcepath[index] = os.path.join(source_path, end_part[index])
        # df.destpath[index] = os.path.join(out_dir, end_part[index])
        # dst = os.path.join(out_dir, subj2, newfilename)
# This chokes because too many open files
        # Thread(target=shutil.copy, args=[src, dst]).start()
        # shutil.copy(src, dst)
        # i += 1
# Uncomment for testing on smaller number of files
        # if i == 10:
        #     break
    tt = time.clock()
    # print("Finished copying %s files in %s min." % (i, ((tt-t)/60)))
# Save newfilename back out to a manifest for later use
    df.to_csv(os.path.join(out_dir, checkname+'manifest_w_sourcedest.csv'),
              index=False)
