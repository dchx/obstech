import glob
import skimage
import numpy as np
import scipy.ndimage as nd
from astropy.io import fits
import matplotlib.pyplot as plt
from skimage.feature.register_translation import _upsampled_dft
'''
object=['m29','standardstar']
band=['b','i','r','v']
filelist=np.tile(['../data/0921/standardstar_b_0.3s-002-subbias-divflat.fit']*10,[len(object),len(band),1])
for i in range(len(object)):
	for j in range(len(band)):
		filelist[i,j]=glob.glob('../data/0921/%s_%s_*-*-subbias-divflat.fit'%(object[i],band[j]))

d0, head = fits.getdata(filelist[0,0,0], header = True)
x = head['NAXIS1']
y = head['NAXIS2']
data = np.zeros([10,y,x]) #data.shape==(10, 1020, 1530)
for i in range(len(object)):
	for j in range(len(band)):
		kaitou=filelist[i,j,0][0:filelist[i,j,0].index('s-')+1]
		outname=kaitou+'-subbias-divflat-comb.fit'
		for k in range(10):
			data[k,:,:],header=fits.getdata(filelist[i,j,k],header=True)
		fid=4;krange=range(10);krange.remove(fid)
		for k in krange:
			shift,error,diffphase=skimage.feature.register_translation\
			                      (data[fid,:,:],data[k,:,:],upsample_factor=1000.)
			print shift,error
			data[k,:,:]=nd.shift(data[k,:,:],shift)
		datamed=np.median(data,axis=0)
		fits.writeto(outname,datamed,header=header,clobber=True)
'''
img1,hd=fits.getdata(glob.glob('../data/0921/m29_i*subbias-divflat-comb.fit')[0],header=True)
img2,hd=fits.getdata(glob.glob('../data/0921/m29_v*subbias-divflat-comb.fit')[0],header=True)
im2o=glob.glob('../data/0921/m29_v*subbias-divflat-comb.fit')[0][0:-4]+'aligntoi.fit'
shift,error,diffphase=skimage.feature.register_translation\
					  (img1,img2,upsample_factor=1000.)
print shift,error
img2=nd.shift(img2,shift)
fits.writeto(im2o,img2,header=hd,clobber=True)

'''
plt.figure(figsize=(12,8))
plt.imshow(data1-data3)
plt.show()
'''