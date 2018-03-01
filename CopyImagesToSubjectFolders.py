import pandas as pd
import sys
import os
import shutil
import datetime
from threading import Thread

""" Take manifest showing tagged files and copy them into folders by subject."""

filename_pattern = '<ck>_<cname>_<datetaken>_<num>.jpg'
out_path = r'E:\UNPROCESSED'
train_folder = 'train1'


def date_to_string(dateobj, format):
    """ Convert to string from datetime."""
    return datetime.datetime.strftime(dateobj, format)


def multi_replace(text, dictobj):
    """Replace characters in the text based on the given dictionary."""
    for k, v in dictobj.iteritems():
        text = text.replace(k, v)
    return text


def fileNewname(out_path, ck, camname, datetime, num):
    """Replace old filename with one based on check, camera name and date/time."""
    # Key, value pairs of what to replace.
    dictobj = {
        '<num>': str(num),
        '<datetaken>': datetime,
        '<cname>': camname,
        '<ck>': check
    }
    # Rename
    new_filename = os.path.join(out_path,
                                multi_replace(filename_pattern, dictobj))
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
    if os.path.exists(out_path):
        print("Output path Ok!\n")
    else:
        print("%s does not exist.\n" % out_path)
        sys.exit("Bad output path!")

    check = os.path.basename(os.path.split(manifest)[0])
    print("Check name: %s\n" % check)

    out_dir = os.path.join(out_path, train_folder)
    try:
        os.makedirs(out_dir)
    except OSError:
        if not os.path.isdir(out_dir):
            raise
    checkname = sys.argv[1]
# Read data into a panda
    df = pd.read_csv(manifest,parse_dates=['datetimeoriginal'])
# Remove rows with no tag
    df = df[df.subject2.notna()]

# Create directories for image copies, if they don't exist
    for subj in df.subject2.unique():
        subj_dir = os.path.join(out_dir, subj)
        try:
            os.makedirs(subj_dir)
        except OSError:
            if not os.path.isdir(subj_dir):
                raise

# Do the copying using threading
    i = 1
    for index, row in df.iterrows():
        subj2 = row['subject2']
        src = row['path']
        dst = fileNewname(os.path.join(out_dir, subj2),
                          checkname, row['camera'],
                          date_to_string(row['datetimeoriginal'],
                          '%Y%m%d__%H_%M_%S'), i)
        Thread(target=shutil.copy, args=[src, dst]).start()
        i += 1
        if i == 10:
            exit()
