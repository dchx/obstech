'''

AST 4723/6725 Coding Mini-Homework 
Due 10/13/2016

Write a script that creates a median image from a list of input images. The 
script should be written in python, but for those of you in AST 4723 you may 
use calls to pyraf routines if you wish [For importing pyraf, use "from pyraf 
import iraf"]. You should not hardwire the filenames into the script, but 
should instead permit this to be an input. One way to do this is to use glob 
to generate a list of all fits files in the directory with names containing 
strings matching some requested input that contains wildcards 
(e.g. *dark*10s*fits). Such a string can also be fed directly to pyraf 
routines. If you already have RHO data, you can use this opportunity to 
generate your master darks. If you do not yet have RHO data, you can obtain 
a copy from another student for now.

You only need to turn in your script, and can do this via email.

'''

import glob
import numpy as np
from astropy.io import fits

type = raw_input("Please input image type \
\n('dark', 'flat', 'standardstar' or object name): ")
expt = raw_input("Please input exposure time ('*s'): ")
if type == 'dark':
	filenames = '../data/0921/%s_%s*.fit' % (type, expt)
	medname = '../data/0921/%s_%s_median.fit' % (type, expt)
else:
	filter = raw_input("Please input filter ('b', 'v', 'r' or 'i'): ")
	filenames = '../data/0921/%s_%s_%s*.fit' % (type, filter, expt)
	medname = '../data/0921/%s_%s_%s_median.fit' % (type, filter, expt)
filelist=glob.glob(filenames)

d0, head = fits.getdata(filelist[0], header = True)
x = head['NAXIS1']
y = head['NAXIS2']
data = np.zeros([np.size(filelist), y, x])

for i in range(np.size(filelist)):
	data[i, :, :], header = fits.getdata(filelist[i], header = True)

datamed=np.median(data,axis=0)
fits.writeto(medname, datamed, clobber=True)