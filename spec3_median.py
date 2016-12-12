import glob
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

imgtype =['alphaOph','altair','argon','epsCyg','neon','Vega']
filenames=[]
filelist=[]
outlist=[]
for i in range(np.size(imgtype)):
	filenames.append('../data/1013/%s_*_*-subbias.fit' % (imgtype[i]))
	filelist.append(glob.glob(filenames[i]))

d0, head = fits.getdata(filelist[0][0], header = True)
x = head['NAXIS1']
y = head['NAXIS2']
data = np.zeros(np.shape(filelist)+(y, x))

for i in range(np.shape(filelist)[0]):
	for j in range(np.shape(filelist)[1]):
		data[i, j, :, :], header = fits.getdata(filelist[i][j], header = True)
	datamed=np.median(data[i, :, :, :],axis=0)
	outname=filelist[i][j][0:filelist[i][j].index('s_')+1]+'-comb.fit'
	fits.writeto(outname, datamed, header=header, clobber=True)

'''
d0, head = fits.getdata('../data/1013/altair_60s_001.FIT', header = True)
x = head['NAXIS1']
y = head['NAXIS2']
data = np.zeros([5, y, x])
for i in range(5):
    data[i, :, :], header = fits.getdata('../data/1013/altair_60s_00%s.FIT'%(i+1), header = True)
datamed=np.median(data,axis=0)
spec=np.mean(datamed,axis=0)
plt.plot(spec/spec.max())
plt.ylim([spec.min()/spec.max(),1])
plt.savefig('plt_altair.png')
plt.close()

d0, head = fits.getdata('../data/1013/Vega_40s_001.FIT', header = True)
x = head['NAXIS1']
y = head['NAXIS2']
data = np.zeros([5, y, x])
for i in range(5):
    data[i, :, :], header = fits.getdata('../data/1013/Vega_40s_00%s.FIT'%(i+1), header = True)
datamed=np.median(data,axis=0)
spec=np.mean(datamed,axis=0)
plt.plot(spec/spec.max())
plt.ylim([spec.min()/spec.max(),1])
plt.savefig('plt_vega.png')
plt.close()

d0, head = fits.getdata('../data/1013/epsCyg_120s_001.FIT', header = True)
x = head['NAXIS1']
y = head['NAXIS2']
data = np.zeros([5, y, x])
for i in range(5):
    data[i, :, :], header = fits.getdata('../data/1013/epsCyg_120s_00%s.FIT'%(i+1), header = True)
datamed=np.median(data,axis=0)
spec=np.mean(datamed,axis=0)
plt.plot(spec/spec.max())
plt.ylim([spec.min()/spec.max(),1])
plt.savefig('plt_epsCyg.png')
plt.close()

d0, head = fits.getdata('../data/1013/alphaOph_100s_001.FIT', header = True)
x = head['NAXIS1']
y = head['NAXIS2']
data = np.zeros([5, y, x])
for i in range(5):
    data[i, :, :], header = fits.getdata('../data/1013/alphaOph_100s_00%s.FIT'%(i+1), header = True)
datamed=np.median(data,axis=0)
spec=np.mean(datamed,axis=0)
plt.plot(spec/spec.max())
plt.ylim([spec.min()/spec.max(),1])
plt.savefig('plt_alphaOph.png')
plt.close()
'''