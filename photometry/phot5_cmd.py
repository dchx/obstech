import glob
import numpy as np
import matplotlib.pyplot as plt
from isochrones.mist import MIST_Isochrone

#obj=['m29','standardstar']
#band=['b','i','r','v']
m29t=30.
sdst=[0.3,0.1,0.1,0.1]
path=('/Users/dong/Documents/Courses/ObsTech/ObservingProject/data/0921/')
dtnms=[glob.glob(path+'m29*.txt'),glob.glob(path+'standard*.txt')]
m29=[np.loadtxt(dtnms[0][i]) for i in range(len(dtnms[0]))]
sds=[np.loadtxt(dtnms[1][i]) for i in range(len(dtnms[0]))]
sdsdat=np.zeros([len(sds),sds[0].shape[1]])
for i in range(len(sds)):
	number,ext_number,flux_iso,fluxerr_iso,flux_isocor,fluxerr_isocor,flux_best,fluxerr_best,xpeak_image,ypeak_image=tuple(sds[i].transpose())
	maxi=np.argmax(flux_iso)
	sdsdat[i]=sds[i][maxi]

sdsmag={'b':3.96,'i':3.89,'r':3.89,'v':3.94}
sdsmag=[3.96,3.89,3.89,3.94]
'''
Ducati, J. R. 2002, yCat, 2237, 0
@ARTICLE{2002yCat.2237....0D,
   author = {{Ducati}, J.~R.},
    title = "{VizieR Online Data Catalog: Catalogue of Stellar Photometry in Johnson's 11-color system.}",
  journal = {VizieR Online Data Catalog},
 keywords = {Photometry: UBVRIJKLMNH},
     year = 2002,
   volume = 2237,
   adsurl = {http://adsabs.harvard.edu/abs/2002yCat.2237....0D},
  adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
'''
number,ext_number,flux_iso,fluxerr_iso,flux_isocor,fluxerr_isocor,flux_best,fluxerr_best,xpeak_image,ypeak_image=tuple([[i,i,i,i] for i in range(m29[0].shape[1])])
mag=[0,0,0,0]
mag_err=[0,0,0,0]
for i in range(len(m29)):
	number[i],ext_number[i],flux_iso[i],fluxerr_iso[i],flux_isocor[i],fluxerr_isocor[i],flux_best[i],fluxerr_best[i],xpeak_image[i],ypeak_image[i]=tuple(m29[i].transpose())
flux_best[3]=flux_best[3][np.where(flux_best[3]>0)]
flux_best[1]=flux_best[1][np.where(flux_best[3]>0)]
fluxerr_best[3]=fluxerr_best[3][np.where(flux_best[3]>0)]
fluxerr_best[1]=fluxerr_best[1][np.where(flux_best[3]>0)]
for i in range(len(m29)):
	flux_ratio=flux_best[i]/m29t/sdsdat[i][6]*sdst[i]
	l=flux_best[i];ls=sdsdat[i][6];sl=fluxerr_best[i];sls=sdsdat[i][7]
	flux_ratio_err=sdst[i]/m29t*l/ls*np.sqrt((sl/l)**2+(sls/ls)**2)
	mag[i]=sdsmag[i]-2.5*np.log10(flux_ratio)
	mag_err[i]=2.5*flux_ratio_err/flux_ratio/np.log(10)

DM=10.94
'''
Strai{\v z}ys, V., Mila{\v s}ius, K., Boyle, R. P., et al. 2014, AJ, 148, 89
@ARTICLE{2014AJ....148...89S,
   author = {{Strai{\v z}ys}, V. and {Mila{\v s}ius}, K. and {Boyle}, R.~P. and 
	{Vrba}, F.~J. and {Munari}, U. and {Walborn}, N.~R. and {{\v C}ernis}, K. and 
	{Kazlauskas}, A. and {Zdanavi{\v c}ius}, K. and {Janusz}, R. and 
	{Zdanavi{\v c}ius}, J. and {Laugalys}, V.},
    title = "{The Enigma of the Open Cluster M29 (NGC 6913) Solved}",
  journal = {\aj},
archivePrefix = "arXiv",
   eprint = {1407.6291},
 primaryClass = "astro-ph.SR",
 keywords = {open clusters and associations: individual: M29 NGC 6913 Cyg OB1, stars: fundamental parameters},
     year = 2014,
    month = nov,
   volume = 148,
      eid = {89},
    pages = {89},
      doi = {10.1088/0004-6256/148/5/89},
   adsurl = {http://adsabs.harvard.edu/abs/2014AJ....148...89S},
  adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
'''
V=mag[3];Verr=mag_err[3]
I=mag[1];Ierr=mag_err[1]
V_Ierr=np.sqrt(Verr**2+Ierr**2)
#------------------isochrones-------------------
iso=MIST_Isochrone(bands=['V','i'])
model = iso.isochrone(7.)
model_v = model.V_mag
model_i = model.i_mag

#------------------plot apparent-------------------
plt.figure()
plt.errorbar(V-I,V,xerr=V_Ierr,yerr=Verr,fmt='k.')
plt.plot(V-I,V,'r.')
plt.axis([-10,15,8,26 ])
plt.gca().invert_yaxis()
plt.xlabel('$V-I$')
plt.ylabel('$V$')
plt.savefig('cmd-allerr.pdf')
plt.close()

id=np.intersect1d(np.where(Verr<1.)[0],np.where(V_Ierr<1.)[0])
V=V[id];Verr=Verr[id];I=I[id];V_Ierr=V_Ierr[id]
plt.figure()
plt.errorbar(V-I,V,xerr=V_Ierr,yerr=Verr,fmt='k.')
plt.plot(V-I,V,'r.')
#plt.axis([-10,15,2,20])
plt.gca().invert_yaxis()
plt.xlabel('$V-I$')
plt.ylabel('$V$')
plt.savefig('cmd-errlt1.pdf')
plt.close()

id=np.intersect1d(np.where(Verr<0.5)[0],np.where(V_Ierr<0.5)[0])
V=V[id];Verr=Verr[id];I=I[id];V_Ierr=V_Ierr[id]
plt.figure()
plt.errorbar(V-I,V,xerr=V_Ierr,yerr=Verr,fmt='k.')
plt.plot(V-I,V,'r.')
#plt.axis([-10,15,2,20])
plt.gca().invert_yaxis()
plt.xlabel('$V-I$')
plt.ylabel('$V$')
plt.savefig('cmd-errlt0.5.pdf')
plt.close()

#------------------plot absolute-------------------
V=mag[3];Verr=mag_err[3]
I=mag[1];Ierr=mag_err[1]
V_Ierr=np.sqrt(Verr**2+Ierr**2)
plt.figure()
plt.errorbar(V-I,V-DM,xerr=V_Ierr,yerr=Verr,fmt='k.')
plt.plot(V-I,V-DM,'r.')
plt.axis([-10,15,-5,15])
plt.gca().invert_yaxis()
plt.xlabel('$V-I$')
plt.ylabel('$M_V$')
plt.savefig('cmdab-allerr.pdf')
plt.close()

id=np.intersect1d(np.where(Verr<1.)[0],np.where(V_Ierr<1.)[0])
V=V[id];Verr=Verr[id];I=I[id];V_Ierr=V_Ierr[id]
plt.figure()
plt.errorbar(V-I,V-DM,xerr=V_Ierr,yerr=Verr,fmt='k.')
plt.plot(V-I,V-DM,'r.')
#plt.axis([-10,15,2,20])
plt.gca().invert_yaxis()
plt.xlabel('$V-I$')
plt.ylabel('$M_V$')
plt.savefig('cmdab-errlt1.pdf')
plt.close()

id=np.intersect1d(np.where(Verr<0.5)[0],np.where(V_Ierr<0.5)[0])
V=V[id];Verr=Verr[id];I=I[id];V_Ierr=V_Ierr[id]
plt.figure()
plt.errorbar(V-I,V-DM,xerr=V_Ierr,yerr=Verr,fmt='k.')
plt.plot(V-I,V-DM,'r.')
#plt.axis([-10,15,2,20])
plt.gca().invert_yaxis()
plt.xlabel('$V-I$')
plt.ylabel('$M_V$')
plt.savefig('cmdab-errlt0.5.pdf')
plt.close()