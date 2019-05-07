#wavelength solution
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib import gridspec
from lmfit import minimize, Parameters

def linelmfit(x, p):
	k, b=p['k'],p['b']
	return k*x+b
def residualslmfit(p, y, x):
	return y - linelmfit(x, p)

pt='../data/1013/'
neonname='neon_5s-comb-spec.fit'
argoname='argon_5s-comb-spec.fit'
neonim=fits.getdata(pt+neonname)/5.
argoim=fits.getdata(pt+argoname)/5.

neon=np.mean(neonim,axis=0)
argo=np.mean(argoim,axis=0)

x=np.arange(neon.size)+1

xne=[]
lne=np.r_[4704.3949,5330.7775,5400.5618,5656.6588]
xne.append(x[489:510][neon[489:510].argmax()])
xne.append(x[179:210][neon[179:210].argmax()])
xne.append(x[159:180][neon[159:180].argmax()])
xne.append(x[39:50][neon[39:50].argmax()])
xne=np.r_[xne]

xar=[]
lar=np.r_[4158.59,4200.674,4272.169,4300.101,4333.561,4510.733]
xar.append(x[759:770][argo[759:770].argmax()])
xar.append(x[739:750][argo[739:750].argmax()])
xar.append(x[699:720][argo[699:720].argmax()])
xar.append(x[689:700][argo[689:700].argmax()])
xar.append(x[669:680][argo[669:680].argmax()])
xar.append(x[584:600][argo[669:680].argmax()])
xar=np.r_[xar]

#line fitting
p0=Parameters()
p0.add('k',value=-2.)
p0.add('b',value=5000.)
#p0['k'].vary=False
out=minimize(residualslmfit,p0,args=(np.r_[lne,lar],np.r_[xne,xar]))#y,x
out0=out.params
print ' k = %.2f +/- %.3f\n'%(out.params['k'].value, out.params['k'].stderr)
print ' b = %.2f +/- %.3f\n'%(out.params['b'].value, out.params['b'].stderr)
l=linelmfit(x,out.params)
lnefit=linelmfit(xne,out.params)
larfit=linelmfit(xar,out.params)

plt.figure(figsize=(8, 8))
gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1]) 
plt1=plt.subplot(gs[0])
plt1.plot(x,l,'k')
plt1.plot(xne,lne,'ok',label='Ne',fillstyle='none',mew=1.5,ms=7)
plt1.plot(xar,lar,'sk',label='Ar',fillstyle='none',mew=1.5,ms=7)
plt1.legend(loc=1)
plt1.axis([1,800,4000,5800])
plt1.set_xticklabels([])
plt1.set_ylabel('wavelength ($\AA$)')
#residual
plt2=plt.subplot(gs[1])
plt2.plot(x,np.zeros(x.size),'k')
#plt2.plot(np.r_[xne,xar],np.r_[lne,lar]-np.r_[lnefit,larfit],'ok')
plt2.plot(xne,lne-lnefit,'ok',label='Ne',fillstyle='none',mew=1.5,ms=7)
plt2.plot(xar,lar-larfit,'sk',label='Ar',fillstyle='none',mew=1.5,ms=7)
plt2.set_yticklabels(['','      -4','-2','0','2','4'])
plt2.axis([1,800,-6,6])
plt2.set_xlabel('x (pixel)')
plt2.set_ylabel('residuals ($\AA$)')
plt.subplots_adjust(hspace=0)
plt.savefig('wlsltn_fit.pdf')
plt.close()

plt.figure(figsize=(10,10))
plt1=plt.subplot(211)
plt1.plot(x,neon,'k')
plt1.plot(xne,neon[xne-1],'|k')
for i in range(lne.size):
	plt1.text(xne[i],neon[xne-1][i]+2.,'%.2f$\AA$'%lne[i],ha='center')
plt1.text(750,180,'Ne',ha='center',fontsize=20)
plt1.set_xticklabels([])
plt1.set_ylabel('counts / exptime (DN/s)')
plt1.axis([1,800,0,200.])#[1,1530,0,1000]
#plt1.invert_xaxis()
plt2=plt.subplot(212)
plt2.plot(x,argo,'k')
plt2.plot(xar,argo[xar-1],'|k')
for i in range(xar.size):
	plt2.text(xar[i],argo[xar-1][i]+2.,'%.2f$\AA$'%lar[i],ha='center')
plt2.text(50,180,'Ar',ha='center',fontsize=20)
#plt2.plot(larfit,argo[xar-1],'o')
plt2.plot(lar,argo[xar-1],'o')
plt2.set_xlabel('x (pixel)')
plt2.set_ylabel('counts / exptime (DN/s)')
#plt2.invert_xaxis()
plt2.axis([1,800,0,200.])
plt.subplots_adjust(hspace=0)
plt.savefig('wlsltn_sed.pdf')
