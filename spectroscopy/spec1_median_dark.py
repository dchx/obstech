import glob
import numpy as np
from astropy.io import fits

exptime=['5s','40s','60s','100s','120s']
filelist=[]
for j in range(len(exptime)):
	filenames='../data/1013/dark_%s_*.FIT'%exptime[j]
	filelist=glob.glob(filenames)
	medname=filelist[0][0:filelist[0].index('s_')+1]+'_median.FIT'

	d0, head = fits.getdata(filelist[0], header = True)
	x = head['NAXIS1']
	y = head['NAXIS2']
	data = np.zeros([np.size(filelist), y, x])

	for i in range(np.size(filelist)):
		data[i, :, :], header = fits.getdata(filelist[i], header = True)

	datamed=np.median(data,axis=0)
	fits.writeto(medname, datamed, clobber=True)