import os
# import shutil
import pandas as pd

""" Get filenames and dirs from folder used to train transfer model and create a manifest. """

# This should not be as useful now that SubsampleFolders.py generates a
#   manifestself.
# Output from this can be used to move files out to another location to make
#   separate training and test sets.

low_number = 1000
random_amount = 1000

# These dirs all need to exist
root_dir = r'E:\UNPROCESSED\train1'
input_dir = r'E:\UNPROCESSED\train1_1000_test_Others'
output_dir = r'E:\UNPROCESSED\train1_manifests'
output_dir2 = r'E:\UNPROCESSED\train1_1000_training'
outfilename = 'train1_1000_test_Others_manifest.csv'
df = pd.DataFrame(columns=["Subdir","Filepath","File","Destpath"])

for folder in os.listdir(input_dir):

	dst = os.path.join(output_dir2, folder)
	src = os.path.join(input_dir, folder)
	src2 = os.path.join(root_dir, folder)
	files = [file for file in os.listdir(src) if os.path.isfile(os.path.join(src, file))] # This does not work, though it would be nice. python 3 construct? file[-4:].lower in ('.jpg','.png')

	for file in files:
		filepath = os.path.join(src2, file)
		fileoutpath = os.path.join(dst, file)
		df = df.append({"Subdir": folder, "Filepath": filepath, "File": file, "Destpath": fileoutpath}, ignore_index=True)
df_outpath = os.path.join(output_dir, outfilename)
df.to_csv(df_outpath, mode='w', index=False, header=True)
