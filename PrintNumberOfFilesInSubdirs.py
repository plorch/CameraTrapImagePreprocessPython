import os

""" Print number of files in subdirs."""

path = r'E:\UNPROCESSED\train1'

folders = ([name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name))]) # get all directories

for folder in folders:
    contents = os.listdir(os.path.join(path, folder))  # get list of contents
    print(folder, len(contents))
