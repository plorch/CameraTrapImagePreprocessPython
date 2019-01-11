import os
# the if in the for below may be a python 3 thing
files = [ f for f in os.listdir('.') if f[-4:].lower in ('.jpg','.png') ]

DRYRUN=True

for (index,filename) in enumerate(files):
  extension = os.path.splitext(filename)[1]
  newname = "picture-%05d.%s" % (index,extension)
  if os.path.exists(newname):
    print "Cannot rename %s to %s, already exists" % (filename,newname)
    continue
  if DRYRUN:
    print "Would rename %s to %s" % (filename,newname)
  else:
    print "Renaming %s to %s" % (filename,newname)
    os.rename(filename,newname)