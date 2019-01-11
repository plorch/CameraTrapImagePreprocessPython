import os
import errno
import shutil

""" Find and delete empty direcotries. """
# Only use this if you want to get rid of the original directories that are empty.

# These dirs all need to exist
root_dir = r'E:\UNPROCESSED\test' # 'E:\UNPROCESSED\train1_1000'

for folder in os.listdir(root_dir):
	src = os.path.join(root_dir, folder)
	try:
		os.rmdir(src)
	except OSError as ex:
		if ex.errno == errno.ENOTEMPTY:
			print "directory not empty"
