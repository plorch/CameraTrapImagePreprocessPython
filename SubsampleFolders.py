import os
import shutil
import random

low_number = 200
random_amount = 500


root_dir = r'/home/leonardo/Desktop/python_script/rfe'
output_dir = r'/home/leonardo/Desktop/python_script/output_folder'

for folder in os.listdir(root_dir):

	dst = os.path.join(output_dir, folder)
	if not os.path.exists(dst):
    	os.mkdir(dst)

	src = os.path.join(root_dir, folder)
	files = [file for file in os.listdir(src) if os.path.isfile(os.path.join(src, file))]
	if len(files) < low_number:
	    for file in files:
	        shutil.copyfile(os.path.join(src, file), dst)
	else:
	    # Amount of random files you'd like to select
	    for x in xrange(random_amount):
	        if len(files) == 0:
	            break
	        else:
	            file = random.choice(files)
	            shutil.copyfile(os.path.join(src, file), dst)