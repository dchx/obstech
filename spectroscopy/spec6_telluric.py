import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib import gridspec
import astropy.constants as ct
import astropy.units as u
from lmfit import minimize, Parameters

#wavelength solotion
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
#wavelength solotion end

tlname='alphaOph_100s-comb-spec.fit'
tlim=fits.getdata(pt+tlname)/100.
tl=np.mean(tlim,axis=0)
exlineindex=np.r_[range(0,383),range(450,641),range(713,758),range(812,826),range(867,1530)]
tlit=tl[exlineindex]
lit=l[exlineindex]

fitindex=np.where(tlit>5.)[0]
tlfit=tlit[fitindex]
lfit=lit[fitindex]

def bbr(l,T):#angatrom, kelvin
	#v=ct.c/(l*u.Angstrom)
	#I=2.*ct.h*v**3./ct.c**2./(np.e**(ct.h*v/ct.k_B/(T*u.Kelvin))-1.)
	a=2.0*ct.h*ct.c**2
	b=ct.h*ct.c/(l*u.Angstrom*ct.k_B*T*u.Kelvin)
	intensity = a/(((l*u.Angstrom)**5)*(np.exp(b)-1.0))
	return intensity #quantity
def bbr2fit(p,l):
	T=p['T'];A=p['A'];B=p['B']	
	return A*bbr(l,T).value+B
def residualsbbr(p,I,l):
	return I / bbr2fit(p,l) -1

#temperature fitting
p0=Parameters()
p0.add('T',value=5500.)
p0.add('A',value=10.**38.)
p0.add('B',value=0.)
#p0['B'].vary=False
out=minimize(residualsbbr,p0,args=(tlfit,lfit))#y,x
out0=out.params
print ' T = %.2f +/- %.3f\n'%(out.params['T'].value, out.params['T'].stderr)
print ' A = %.3e +/- %.3e\n'%(out.params['A'].value, out.params['A'].stderr)
print ' B = %.2f +/- %.3f\n'%(out.params['B'].value, out.params['B'].stderr)
Ibb=bbr2fit(out.params,lfit)
ratioit=np.ones(lit.size)
ratioit[fitindex]=tlfit/Ibb

T=out.params['T'].value
peakl=(ct.b_wien/(T*u.Kelvin)).to(u.Angstrom).value
Ipeak=bbr2fit(out.params,peakl)

plt.figure(figsize=(8,8))
#plt.plot(range(tl.size),tl)#find interpolate index
#plt.show()
plt1=plt.subplot(311)
plt1.plot(l,tl,'--k',label='Before interpolation')#before interpolate
plt1.plot(lit,tlit,'-k',label='After interpolation')#after interpolate
plt1.legend(loc=2,fontsize=12)
plt1.axis([l[1529],l[0],0,65.])
plt1.set_ylabel('counts / exptime (DN/s)')

plt2=plt.subplot(312)
plt2.plot(l,tl,'--k',label='Before interpolation')#before interpolate
plt2.plot(lit,tlit,'-k',label='After interpolation')#after interpolate
plt2.plot(lfit,Ibb,'r',label='Blackbody fit')#blackbody fit curve
plt2.plot([lit[fitindex[-1]],lit[fitindex[-1]]],[0,70],':k')#fit cutoff
plt2.legend(loc=2,fontsize=12)
#plt2.plot(peakl,Ipeak,'ow')# wein displace blackbody peak
#plt2.plot(l[Ibb.argmax()],Ibb.max(),'+k')#blackbody fit curve peak
plt2.axis([l[1529],l[0],0,65.])
plt2.set_ylabel('counts / exptime (DN/s)')

plt3=plt.subplot(313)
plt3.plot(l,np.ones(l.size),'-r')
plt3.plot(lit,ratioit,'-k')#residual ratio
plt3.set_xlabel('wavelength ($\AA$)')
plt3.set_ylabel('residual ratio')
#plt3.axis([l[1529],l[0],-400,400])
plt3.set_xlim([l[1529],l[0]])
plt3.set_yticks(np.arange(0.94,1.06,0.02))
plt.subplots_adjust(hspace=0)
plt.savefig('telluric.pdf')
plt.close()
'''
#block body curve test
lbig=np.linspace(0,20000,1000)
Tbig=5000.#K
plt.plot(lbig,bbr(lbig,Tbig).value)
peakl=(ct.b_wien/(Tbig*u.Kelvin)).to(u.Angstrom).value
plt.plot(peakl,bbr(peakl,Tbig).value,'o')
Tbig=4000.#K
plt.plot(lbig,bbr(lbig,Tbig).value)
peakl=(ct.b_wien/(Tbig*u.Kelvin)).to(u.Angstrom).value
plt.plot(peakl,bbr(peakl,Tbig).value,'o')
Tbig=3000.#K
plt.plot(lbig,bbr(lbig,Tbig).value)
peakl=(ct.b_wien/(Tbig*u.Kelvin)).to(u.Angstrom).value
plt.plot(peakl,bbr(peakl,Tbig).value,'o')
plt.show()
'''