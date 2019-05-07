'''
Exposure time calculator for RHO
Using standard star 58 Cyg
'''
import numpy as np
import matplotlib.pyplot as plt

def exptime(m,c,band): #args=(mag,counts,band)
	bands=np.array(['B','I','R','V'])
	cs=[6.88946600e+05,4.17099500e+05,7.69867400e+05,5.08532200e+05]#counts of 58 Cyg
	cserr=[7.13729200e+01,6.74930200e+01,6.99797700e+01,6.72412800e+01]#counts of 58 Cyg error
	ms=[3.96,3.89,3.89,3.94]#mag of 58 Cyg
	ts=[0.3,0.1,0.1,0.1]#exposure time of 58 Cyg (second)
	i=np.where(bands==band)[0][0]
	t=c/(cs[i]/ts[i]*10**((ms[i]-m)/2.5))
	return t

m=np.linspace(-2,15,100)
plt.figure()
plt.semilogy(m,exptime(m,10000.,'B'),'r',label='$B$')
plt.semilogy(m,exptime(m,10000.,'V'),'c',label='$V$')
plt.semilogy(m,exptime(m,10000.,'R'),'g',label='$R$')
plt.semilogy(m,exptime(m,10000.,'I'),'b',label='$I$')
plt.xlim([-2,15])
plt.legend(loc=0)
plt.xlabel('Apparent magnitude')
plt.ylabel('Exposure time (s)')
plt.grid()
plt.savefig('exptime_calc.pdf')
plt.close()