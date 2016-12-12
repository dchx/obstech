import glob
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

fl=glob.glob('../data/1013/*-comb.fit')
for i in range(len(fl)):
	data,header=fits.getdata(fl[i],header=True)
	outname=fl[i][0:-4]+'-spec.fit'
	fits.writeto(outname, data[399:475,:], header=header, clobber=True)