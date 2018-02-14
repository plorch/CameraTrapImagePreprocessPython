import os,sys
folder = r'C:\Users\pdl\Documents\transfer\C5_checked_MS1135a'
for filename in os.listdir(folder):
       infilename = os.path.join(folder,filename)
       if not os.path.isfile(infilename): continue
       oldbase = os.path.splitext(filename)
       newname = infilename.replace('.JPG', '.jpg')
       output = os.rename(infilename, newname)