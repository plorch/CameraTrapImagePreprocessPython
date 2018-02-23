import os
import sys

# file_to_delete = 'manifest_w_empty.csv'

""" Removes manifest files from subdirectories in a specified dir. """

if __name__ == '__main__':
    file_to_delete = sys.argv[1]
    folderpath = sys.argv[-1]
    print("\nChecking if folder path exists...\n")
    if os.path.exists(folderpath):
        print("Ok!\n")
    else:
        print("%s does not exist.\n" % folderpath)
        sys.exit("Bad path!")
    check = os.path.split(folderpath)[1]
    print("Check name: %s\n" % check)

    cams = os.listdir(folderpath)
    # This avoids walking check directories, looking for images
    for cam in cams:
        campath = os.path.join(folderpath, cam)
        file_td = os.path.join(campath, file_to_delete)
        try:
            os.remove(file_td)
            print("Delete %s in %s\n" % (file_to_delete, cam))
        except OSError:
            pass
