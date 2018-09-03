import os
import shutil
import random

low_number = 1000
random_amount = 1000


root_dir = r'E:\UNPROCESSED\train1'
output_dir = r'E:\UNPROCESSED\train1_1000'

for folder in os.listdir(root_dir):

	dst = os.path.join(output_dir, folder)
	if not os.path.exists(dst):
		os.mkdir(dst)

	src = os.path.join(root_dir, folder)
	files = [file for file in os.listdir(src) if os.path.isfile(os.path.join(src, file))]
	if len(files) < low_number:
		for file in files:
			shutil.copyfile(os.path.join(src, file), os.path.join(dst,file))
	else:
		# Amount of random files you'd like to select
		# Use xrange if running with python 2 (e.g., py -2 SubsampleFolders.py)
#		for x in xrange(random_amount):
#		 use range if running with python 3 (e.g., py -2 SubsampleFolders.py)
		for x in range(random_amount):
			if len(files) == 0:
				break
			else:
				file = random.choice(files)
				shutil.copyfile(os.path.join(src, file), os.path.join(dst,file))
