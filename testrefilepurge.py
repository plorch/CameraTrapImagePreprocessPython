import os
import re

def purge(dir, pattern):
    for f in os.listdir(dir):
    	if re.match(pattern, f):
    		os.remove(os.path.join(dir, f))

if __name__ == '__main__':
    dirname=r"P:\testimageprocessing\tester"
    delpat="\._"
    purge(dirname,delpat)