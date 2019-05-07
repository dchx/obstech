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
print ' k = %.4f \pm %.3f\n'%(out.params['k'].value, out.params['k'].stderr)
print ' b = %.2f \pm %.3f\n'%(out.params['b'].value, out.params['b'].stderr)
l=linelmfit(x,out.params)
lerr=residualslmfit(out.params, np.r_[lne,lar], np.r_[xne,xar]).std()
#wavelength solotion end

#tulluric correction
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
print ' T = %.2f \\pm %.3f\n'%(out.params['T'].value, out.params['T'].stderr)
print ' A = %.4e \\pm %.3e\n'%(out.params['A'].value, out.params['A'].stderr)
print ' B = %.2f \\pm %.3f\n'%(out.params['B'].value, out.params['B'].stderr)
Ibb=bbr2fit(out.params,lfit)
ratioit=np.ones(lit.size)
ratioit[fitindex]=tlfit/Ibb
#telluric correction end

itpindex=np.setdiff1d(np.arange(l.size),exlineindex)
itpratio=np.zeros(itpindex.size)
for i in range(itpindex.size):
	itpratio[i]=np.interp(l[itpindex][i],lit[lit.argsort()],ratioit[lit.argsort()])
ratio=np.ones(l.size)
ratio[exlineindex]=ratioit
ratio[itpindex]=itpratio

filelist=[pt+'Vega_40s-comb-spec.fit',
 pt+'altair_60s-comb-spec.fit',
 pt+'epsCyg_120s-comb-spec.fit']
exptime=np.r_[40.,60.,120.]

d0, head = fits.getdata(filelist[0], header = True)
x = head['NAXIS1']
y = head['NAXIS2']
data = np.zeros(np.shape(filelist)+(y, x))
for i in range(np.shape(filelist)[0]):
	data[i,:,:] = fits.getdata(filelist[i])/exptime[i]
spec=np.mean(data,axis=1)
specerr=np.std(data,axis=1)

#-------------------Equivalent width---------------------#
#l,lerr,spec,specerr
dl=-np.diff(l).mean()
dist=np.r_[25.04,16.73,72.7]#ly

lineindex=[]
#vega: H_beta,H_gamma,..,..,..
lineindex.append((range(405,447),range(652,688),range(754,813),range(836,872),range(886,906)))
#altair: H_beta,H_gamma,..,..,..
lineindex.append((range(403,453),range(662,687),range(772,813),range(832,868),range(886,909)))
#eCyg: 
lineindex.append((range(157,176),range(220,243),range(262,283),range(416,432),range(685,703)))
minl=np.zeros(np.shape(lineindex))
specmin=np.zeros(np.shape(lineindex))
ratiomin=np.zeros(np.shape(lineindex))
eqw=np.zeros(np.shape(lineindex))
eqwerr=np.zeros(np.shape(lineindex))
for i in range(len(lineindex)):
	for j in range(len(lineindex[i])):
		lline=l[lineindex[i][j]]
		specline=spec[i][lineindex[i][j]]
		speclineerr=specerr[i][lineindex[i][j]].std()
		ratioline=ratio[lineindex[i][j]]
		spec0=np.interp(lline,lline[[-1,0]],specline[[-1,0]])
		eqw[i,j]=np.sum((1.-specline/spec0)*dl)
		eqwerr[i,j]=np.sqrt(sum((1+(specline/spec0)**2)*lerr**2+(dl/spec0*speclineerr)**2))/spec0.size
		minl[i,j]=lline[specline.argmin()]
		specmin[i,j]=specline.min()
		ratiomin[i,j]=ratioline[specline.argmin()]
linename=[['H$\\beta$','H$\\gamma$','H$\\delta$','H$\\varepsilon$','H$\\zeta$'],
 ['H$\\beta$','H$\\gamma$','H$\\delta$','H$\\varepsilon$','H$\\zeta$'],
 ['FeI','CaI','MgI','KI','FeI']]
print 'line,wavelength,equivalent width'
for i in range(minl.shape[0]):
	print filelist[i]
	for j in range(minl.shape[1]):
		print '%s\t & %.1f & $%.2f \\pm %.2f$'%(linename[i][j],minl[i,j],eqw[i,j],eqwerr[i,j])

#-------------plots---------------------
fi,pltarr = plt.subplots(3,1,figsize=(8,8),sharex=True)#, sharex=True, sharey=True
fi.subplots_adjust(hspace=0)
fi.text(0.04, 0.5, 'counts / exptime (DN/s)', ha='center', va='center', rotation='vertical')
for i in range(np.shape(spec)[0]):
	pltarr[i].plot(l,spec[i],'r',linewidth=0.5,label='Before correction')
	pltarr[i].plot(l,spec[i]/ratio,'k',label='After correction')
	pltarr[i].legend(loc=2,fontsize=12)
	#if i!=2:pltarr[i].set_xticklabels([])
	#if i!=2:pltarr[i].get_xaxis().set_visible(False)
for j in range(minl[0].size):
	pltarr[0].text(minl[0][j],specmin[0][j]/ratiomin[0,j]-30.,linename[0][j],ha='center')
	pltarr[1].text(minl[1][j],specmin[1][j]/ratiomin[1,j]-15.,linename[1][j],ha='center')
	pltarr[2].text(minl[2][j],specmin[2][j]/ratiomin[2,j]-2.5,linename[2][j],ha='center')
pltarr[0].set_yticks([0,100,200,300,400]);pltarr[0].set_ylim([0,400])
pltarr[1].set_yticks([0,50,100,150,200]);pltarr[1].set_ylim([0,215])
pltarr[2].set_yticks([0,5,10,15,20,25]);pltarr[2].set_ylim([0,30])
pltarr[2].set_xlabel('wavelength ($\AA$)')
fi.text(0.15,0.67,'Vega')
fi.text(0.15,0.4,'Altair')
fi.text(0.15,0.13,'$\\varepsilon$ Cyg')
plt.xlim([l[1529],l[0]])
plt.savefig('plot_spec_comp.pdf')
plt.close()

plt.figure()
for i in range(np.shape(spec)[0]):
	plt.plot(l,spec[i]/ratio,'k')
for j in range(minl[1].size):
	plt.text(minl[1][j]+50.,specmin[1][j]/ratiomin[1,j]-12.,linename[1][j],ha='center')
plt.xlabel('wavelength ($\AA$)')
plt.ylabel('counts / exptime (DN/s)')
plt.axis([l[1529],l[0],0,400])
plt.text(5500,350,'Vega')
plt.text(5500,180,'Altair')
plt.text(5500,10,'$\\varepsilon$ Cyg')
plt.savefig('plot_spec_tog.pdf')
plt.close()

plt.figure()
for i in range(np.shape(spec)[0]):
	plt.plot(l,spec[i]/ratio/dist[i]**2,'k')
for j in range(minl[1].size):
	plt.text(minl[0][j]+50.,specmin[0][j]/ratiomin[0,j]/dist[0]**2-0.03,linename[0][j],ha='center')
plt.xlabel('wavelength ($\AA$)')
plt.ylabel('counts / (exptime * distance$^2$) (DN s$^{-1}$ ly$^{-2}$)')
plt.axis([l[1529],l[0],0,0.8])
plt.text(5500,0.55,'Vega')
plt.text(5500,0.67,'Altair')
plt.text(5500,0.02,'$\\varepsilon$ Cyg')
plt.savefig('plot_spec_tog_ab.pdf')
plt.close()