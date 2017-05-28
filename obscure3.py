import os
from PIL import Image, ImageDraw
import time
''' Speed test 
      Rectangle is faster but may leave underlying image visible to hackers
'''
fpath=r"G:\NaturalResources\Lorch\CMPCameraMonitoring\CameraTrapImagePreprocessPython\imagemaniptest_py\testimages\02150562.JPG"
im=Image.open(fpath)
width=im.size[0]
height=im.size[1]

# These were decided by trial and error using fraction of width and height
x1=int(0.16*width)
x2=int(0.28*width)
y1=int(0.94*height)
y2=int(0.98*height)

#t = time.clock()
#
#pixels=im.load()
#
#for i in range(x1,x2):
#    for j in range(y1,y2):
#        pixels[i,j]=(0,0,0)
#
#tt = time.clock()
#print tt-t #0.051845
#
#im.show()

t = time.clock()

draw = ImageDraw.Draw(im)
draw.rectangle([(x1,y1),(x2,y2)],fill="white")
del draw

tt = time.clock()
print tt-t #0.000141

im.show()
im.save(os.path.join(os.path.dirname(fpath),os.path.splitext(os.path.split(fpath)[1])[0]+"obsc."+os.path.splitext(os.path.split(fpath)[1])[1]))