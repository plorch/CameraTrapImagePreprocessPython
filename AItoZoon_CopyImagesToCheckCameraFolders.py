import pandas as pd
import sys
import os
import shutil
import datetime
import time
from PIL import Image, ImageDraw  # ImageChops,
from PIL.ExifTags import TAGS
# After running pip install progressbar2 or pip install tqdm
# import progressbar
import tqdm
# from threading import Thread

""" Take manifest from AI showing tagged files and copy them into folders by
check and camera in a way that makes sense for future Zoonivers uploads panda
allows tracking back to original. Pathnames on AWS and windows are different
requiring some antics to remake source paths."""

# Calling this program will look like this:
# py -2 .\AItoZoon_CopyImagesToCheckCameraFolders.py 'C22' 'E:\UNPROCESSED\22ndCheckJanuary2018\train_1000_2nd_4_server_weights_predictionsC22_BC.csv'

manifest = sys.argv[-1]
filename_pattern = '<ck>_<cname>_<datetaken>_<num>.jpg'
source_path = os.path.dirname(manifest)
# r'E:\UNPROCESSED\22ndCheckJanuary2018'
zoon_folder = 'zoon_upload'

def get_exif_data(filename):
    """Get embedded EXIF data from image file."""
    # Source: <a href="http://www.endlesslycurious.com/2011/05/11/extracting-image-exif-data-with-python/">http://www.endlesslycurious.com/2011/05/11/extract...</a>

    ret = {}
    try:
        img = Image.open(filename)
        if hasattr(img, '_getexif'):
            exifinfo = img._getexif()
            if exifinfo is not None:
                for tag, value in exifinfo.items():
                    decoded = TAGS.get(tag, tag)
                    ret[decoded] = value
    except IOError:
        print 'IOERROR ' + filename
#    img.close()
    return ret


def get_date_taken(filename):
    """Extract datetime"""
    datestring = get_exif_data(filename)['DateTimeOriginal']
    return datetime.datetime.strptime(datestring, '%Y:%m:%d %H:%M:%S')


def get_filenames(folderpath):  #
    """Get folderpath, make that working directory, and return the list of files.
    """
    os.chdir(folderpath)
    files = os.listdir('.')
    return [i for i in files if os.path.splitext(i)[1].lower() in {'.jpg', '.png'}]


def get_image_paths(folderpath):
    """Get image paths."""
    return (os.path.join(folderpath, f)
            for f in os.listdir(folderpath)
            if os.path.splitext(f)[1].lower() in {'.jpg', '.png'})


def get_numbering_format(digits, num):
    """ Decide on how to do numbering."""
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
    """ Convert to string from datetime."""
    return datetime.datetime.strftime(dateobj, format)


def multi_replace(text, dictobj):
    """Replace characters in the text based on the given dictionary."""
    for k, v in dictobj.iteritems():
        text = text.replace(k, v)
    return text


def image_reduce(img, redfac=2):
    """Reduce image size by redfac to meet Zooniverse 60kb upload limit."""
    w, h = img.size
    size = (int(round(w/redfac)), int(round(h/redfac)))
#   redfac=2 or 50% reduction should give (960,720) which is still big enough to view
    img = img.resize(size, Image.ANTIALIAS)
    return (img)

# Kept here just to help creating fileNewname below
def fileRename(current_file, num, digits):
    """Replace old filename with one based on camera name (dir name) and date/time."""
    # Key, value pairs of what to replace.
    dictobj = {
        '<num>': get_numbering_format(digits, num),
        '<datetaken>': date_to_string(get_date_taken(current_file), '%Y%m%d__%H_%M'),
        '<dname>': dirname,
        '<cname>': camname,
        '<ck>': check
    }
    # Rename
    new_filename = os.path.join(os.path.dirname(current_file),multi_replace(filename_pattern, dictobj))
    shutil.move(current_file, new_filename)
    return(new_filename)


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
#    manifest = sys.argv[-1]
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
# Add places to track sourcefile paths which are different from path on AWS
# For testing: py -2
# import os
# import pandas as pd
# source_path=r'E:\UNPROCESSED\22ndCheckJanuary2018\train_1000_2nd_4_server_weights_predictionsC22_BC.csv'
# df= pd.read_csv(r'E:\UNPROCESSED\22ndCheckJanuary2018\train_1000_2nd_4_server_weights_predictionsC22_BC.csv')
# zoon_folder = 'zoon_upload'
# out_dir = os.path.join(source_path, zoon_folder)

# This pulls off the end part to make a new path name
    end_part = df.file_name.str.split('/', 1, expand=True)[1]
    df['camera'] = df.file_name.str.split('/', 2, expand=True)[1]
# makes new sourcepath from end part
    df['sourcepath'] = end_part.apply(lambda x: os.path.abspath(os.path.join(source_path, x)))
    # df['destpath'] = end_part.apply(lambda x: os.path.abspath(os.path.join(out_dir, x)))
    df['destpath'] = ""
    df['datetimeoriginal'] = ""

# Create directories for image copies, if they don't exist
    for fldr in ('birds', 'squirrels', '10focal_species'):
        fldr_dir = os.path.join(out_dir, fldr)
        try:
            os.makedirs(fldr_dir)
        except OSError:
            if not os.path.isdir(fldr_dir):
                raise

    t = time.clock()
# Do the copying (using threading?)
# The .loc stuff ensures that assignments are done to panda df and not view
# tqdm is to tell progress and estimate time elapsed
    i = 1
    for index, row in tqdm.tqdm(df.iterrows(), total=df.shape[0]):
        subj2 = row['predicted']
        src = row['sourcepath']
        date_str = df.loc[index,'datetimeoriginal'] = date_to_string(get_date_taken(src), '%Y%m%d__%H_%M_%S')
        newfilename = fileNewname(checkname, row['camera'],
                                  date_str, i)
        df.loc[index,'sourcepath'] = os.path.join(source_path, end_part[index])
        if subj2 in ('BIRD', 'TURKEY'):
            df.loc[index,'destpath'] = os.path.join(out_dir, 'birds', newfilename)
        elif subj2 in ('BLWSQL', 'CHIPMK', 'FLYSQL', 'FOXSQL', 'MLGSQL',
                          'GRYSQL', 'REDSQL', 'WDCHUK'):
            df.loc[index,'destpath'] = os.path.join(out_dir, 'squirrels', newfilename)
        elif subj2 in ('CATDOM', 'COYOTE', 'DEER', 'DOGDOM', 'GRFOX',
                          'HUMAN', 'MINK', 'OPOSSM', 'RACOON', 'RDFOX'):
            df.loc[index,'destpath'] = os.path.join(out_dir, '10focal_species', newfilename)
        else:
            df.loc[index,'destpath'] = None
#        dst = os.path.join(out_dir, newfilename)
        if df.loc[index,'destpath'] != None:
            shutil.copy(df.loc[index,'sourcepath'], df.loc[index,'destpath'])
        i += 1
# Uncomment for testing on smaller number of files
#         if i == 10:
#             break
    tt = time.clock()
    print("Finished copying %s files in %s min." % (i, ((tt-t)/60)))
# Save newfilename back out to a manifest for later use
    df.to_csv(os.path.join(out_dir, checkname+'manifest_w_sourcedest.csv'),
              index=False)
