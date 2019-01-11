import os
import pandas as pd

""" Count image files in folders to describe training set size """

ipath = r"E:\UNPROCESSED\train1_1000_test_Others"
totalfiles = 0
df = pd.DataFrame(columns=["Folder", "Count"])

folders = ([name for name in os.listdir(ipath)
            if os.path.isdir(os.path.join(ipath, name))])
for folder in folders:
    contents = os.listdir(os.path.join(ipath, folder))  # get list of contents
    foldercount = len(contents)
    totalfiles = totalfiles + foldercount
    df = df.append({"Folder": folder, "Count": foldercount}, ignore_index=True)
    print(folder, foldercount)
print(totalfiles)
df_outpath = os.path.join(ipath, 'folder_counts_test_Others.csv')
df.to_csv(df_outpath, mode='w', index=False, header=True)
