'''

AST 4723/6725 Coding Mini-Homework 
Due 10/25/2016

Write a script that creates a master flatfield. The script should be written
in python, but for those of you in AST 4723 you may use calls to pyraf routines
if you wish (pyraf.iraf.mscred.flatcombine or pyraf.iraf.images.immatch.imcombine).
You should not hardwire the filenames into the script, but should instead permit 
this to be an input. Because individual flat images may have very different count
levels, it is necessary to normalize thme (multiplicative scaling) to a common 
level before combining them. Your choice of what level you normalize them to at
this stage is arbitrary, but a value of 1 can be useful for simplicity. Once you
have combined them, the final image must be normalized to 1.0.

The specific operations that the script should perform are the following:
1. Read in a list of input files (which should already be bias-subtracted).
2. Compute the median for each input image.
3. Normalize the array associated with each image to have the same median value.
4. Median combine the list of arrays associated with the input images, as in coding
   homework #2.
5. Renormalize this median-combined array to have a median value of 1.
6. Write out the result to a file.

This time, please turn in both the script and your master flatfield via email. Note
that I am not requiring you to show me code for subtracting the master bias. You
will need this at some point, but for now you can do this however you wish.

Bonus: If you want to get a bit further, write a routine to divide the science images
by the flatfield.

Big picture: After this assignment, you will have scripts to generate master darks
and master flats, and if you do the bonus will also be able to apply those flats
(a routine for applying darks should be very similar). At this point you will be well
on your way with the photometry project. The remaining steps will be alignment and
stacking, followed by photometry with Source Extractor.

'''

import glob
import numpy as np
from astropy.io import fits

# Read in a list of input files (which should already be bias-subtracted).
filenames = raw_input("Please input image file names: ") # e.g. '../data/0921/flat_b_*-*-*.fit'
filelist = glob.glob(filenames)

# Compute the median for each input image.
d0, head = fits.getdata(filelist[0], header = True)
x = head['NAXIS1']
y = head['NAXIS2']
data = np.zeros([np.size(filelist), y, x])
datamed = np.zeros(np.size(filelist))
for i in range(np.size(filelist)):
	data[i, :, :], header = fits.getdata(filelist[i], header = True)
	datamed[i] = np.median(data[i, :, :])
	
# Normalize the array associated with each image to have the same median value.
	data[i, :, :] = data[i, :, :] / datamed[i]

# Median combine the list of arrays associated with the input images, as in coding
# homework #2.
datacomb = np.median(data,axis=0)

# Renormalize this median-combined array to have a median value of 1.
datacomb = datacomb / np.median(datacomb)

# Write out the result to a file.
combname = filelist[0][0:filelist[0].index('-')]+'-comb.fit'
#fits.writeto(combname, datacomb, header=header, clobber=True)

# Divide the science images by the flatfield.
objnames = raw_input("Please input object image file names: ") # e.g. '../data/0921/m29_b_*-*-*.fit'
objlist = glob.glob(objnames)
for i in range(np.size(objlist)):
	ft = objlist[i][objlist[i].index('_')+1:objlist[i].index('_')+2]
	flatname = glob.glob('flat_'+ft+'_*-comb.fit')
	data[i, :, :], header = fits.getdata(objlist[i], header = True)
	flat = fits.getdata(flatname[0])
	data[i, :, :] = data[i, :, :] / flat
	dataname = objlist[i][0:len(objlist[i])-4]+'-divflat.fit'
	fits.writeto(dataname, data[i, :, :], header=header, clobber=True)
