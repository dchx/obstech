import glob
import numpy as np
from astropy.io import fits

imgtype =['alphaOph','altair','argon','epsCyg','neon','Vega']
filenames=[]
filelist=[]
biaslist=[]
outlist=[]
for i in range(np.size(imgtype)):
	filenames.append('../data/1013/%s_*_*.FIT' % (imgtype[i]))
	filelist.append(glob.glob(filenames[i]))
	tmp=filelist[i][0]
	biaslist.append('../data/1013/dark'+tmp[tmp.index('_'):tmp.index('_0')]+'_median.FIT')

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