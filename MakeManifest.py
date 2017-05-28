import os, csv

'''Create manifest from file names of reduced files'''
# Calculate entropy and save that in the manifest as a hidden field
# For now assume we are in the right directory, then fix it to work with dir
files = [ f for f in os.listdir('.') if f[-4:].lower() in ('.jpg','.png') ]

# Need to create the manifest name inteligently and put it into the right place

f=open("weights.csv",'r+')
w=csv.writer(f)
# To write the first row
w.writerow(['Image 1','Image 2','Image 3','ID', '#Entropy12', '#Entropy23'])
# Need to figure out how to go through the dir 3 files at a time
for filename in files:
    w.writerow([filename])