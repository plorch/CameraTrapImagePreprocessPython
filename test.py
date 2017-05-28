import os

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


def get_image_paths(fpath=folderpath):
  return (os.path.join(fpath, f) 
      for f in os.listdir(fpath) 
      if os.path.splitext(f)[1].lower() in {'.jpg', '.png'})

if __name__ == '__main__':
    paths=get_image_paths(folderpath)
#    pl=len(','.join(paths))
    print '\n'.join(paths)
    print len(list(paths))
