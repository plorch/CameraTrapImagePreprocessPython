import os
import shutil
import random
import pandas as pd

""" Create training data set by subsampling folders. """

low_number = 1000
random_amount = 2000

root_dir = r'E:\UNPROCESSED\train1_1000_Deer_Coyote'
output_dir = r'E:\UNPROCESSED\train1_1000_test_3rd'
output_dir2 = r'E:\UNPROCESSED\train1_manifests'
outfilename = 'train1_1000_3rd_DEER_manifest.csv'
df = pd.DataFrame(columns=["Subdir","Filepath","File","Destpath"])


for folder in os.listdir(root_dir):

	dst = os.path.join(output_dir, folder)
	if not os.path.exists(dst):
		os.mkdir(dst)

	src = os.path.join(root_dir, folder)
	files = [file for file in os.listdir(src) if os.path.isfile(os.path.join(src, file))]
	if len(files) < low_number:
		for file in files:
			shutil.copyfile(os.path.join(src, file), os.path.join(dst,file))
			df = df.append({"Subdir": folder, "Filepath": os.path.join(src, file), "File": file, "Destpath": os.path.join(dst,file)}, ignore_index=True)
	else:
		# Amount of random files you'd like to select
		# Use xrange if running with python 2 (e.g., py -2 SubsampleFolders.py)
#		for x in xrange(random_amount):
#		 use range if running with python 3 (e.g., py -2 SubsampleFolders.py)
		for x in range(random_amount):
			if len(files) == 0:
				break
			else:
				random.seed() # to get same results, enter an integer here
				file = random.choice(files)
				shutil.copyfile(os.path.join(src, file), os.path.join(dst,file))
				df = df.append({"Subdir": folder, "Filepath": os.path.join(src, file), "File": file, "Destpath": os.path.join(dst,file)}, ignore_index=True)
df_outpath = os.path.join(output_dir2, outfilename)
df.to_csv(df_outpath, mode='w', index=False, header=True)
