import os
import shutil
import pandas as pd

""" Move images out of dirs from where they were copied to build a training dataset. """

output_dir2 = r'E:\UNPROCESSED\train1_1000_training'
manifest = r'E:\UNPROCESSED\train1_manifests\train1000_manifest.csv'
outfilename = 'train1000_manifest2.csv'

# Read data into a panda
df = pd.read_csv(manifest)
# Add place to track new names
df['Copied'] = ""

dirs_needed = df.Destpath.apply(os.path.dirname).unique()

# Create directories for image copies, if they don't exist
for img in dirs_needed:
	try:
		os.makedirs(img)
	except OSError:
		if not os.path.isdir(img):
			raise

# Move the images
for index, row in df.iterrows():
	src = row['Filepath']
	dst = row['Destpath']
	if os.path.exists(src):
		shutil.move(src, dst)
	row['Copied'] = "1"

# Write out what was copied out, in case you want to replace it (reversing src and dst)
df_outpath = os.path.join(os.path.dirname(manifest), outfilename)
df.to_csv(df_outpath, mode='w', index=False, header=True)
