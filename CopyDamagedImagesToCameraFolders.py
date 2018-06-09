import sys
import os
import shutil
# from threading import Thread

""" Take text file showing damaged files and copy them to folders by camera."""

# You can get a list of damaged .jpg files from running badpeggy, selecting
#  all, exporting to text file, putting it in folder with images to be cleaned
#  of damaged images.

#  https://www.coderslagoon.com/#/product/badpeggy

# Calling this program will look like this:
# py -2 .\CopyDamagedImagesToCameraFolders.py 'E:\UNPROCESSED\
# First_three_checks_tagged_and_nothing\B_check_Tagged_and_nothings\
# file_with_bad_files_one_per_row.txt'

out_path = r'E:\UNPROCESSED'

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

    out_dir = os.path.split(manifest)[0] + "_bad"

    try:
        os.makedirs(out_dir)
    except OSError:
        if not os.path.isdir(out_dir):
            raise
    print("Output directory is %s\n" % out_dir)

    for line in manifest:
        camera = os.path.split(os.path.basename(line))[0]
        dest = os.path.join(out_dir, camera)
        if not os.path.isdir(dest):
            try:
                os.makedirs(dest)
            except OSError:
                raise
        shutil.copy(line, dest)

    print("Finished copying bad files.")
