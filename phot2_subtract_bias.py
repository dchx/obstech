import glob
import numpy as np
from astropy.io import fits

imgtype = raw_input("Please input image type \
\n('flat', 'standardstar' or object name): ")
filter = ['b', 'v', 'r', 'i']
filenames=[]
filelist=[]
biaslist=[]
outlist=[]
for i in range(np.size(filter)):
	filenames.append('../data/0921/%s_%s*.fit' % (imgtype, filter[i]))
	filelist.append(glob.glob(filenames[i]))
	tmp=filelist[i][0]
	biaslist.append('../data/0921/dark'+tmp[tmp.index('_')+2:tmp.index('-')]+'_median.fit')

d0, head = fits.getdata(filelist[0][0], header = True)
x = head['NAXIS1']
y = head['NAXIS2']
data = np.zeros(np.shape(filelist)+(y, x))
bias = np.zeros(np.shape(biaslist)+(y, x))

for i in range(np.shape(biaslist)[0]):
	bias[i,:,:] = fits.getdata(biaslist[i])

for i in range(np.shape(filelist)[0]):
	for j in range(np.shape(filelist)[1]):
		data[i, j, :, :], header = fits.getdata(filelist[i][j], header = True)
		data[i, j, :, :] = data[i, j, :, :]-bias[i,:,:]
		outname=filelist[i][j][0:len(filelist[i][j])-4]+'-subbias.fit'
		fits.writeto(outname, data[i,j,:,:], header=header, clobber=True)