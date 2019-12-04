import numpy as np

def multivariate_gaussian(r, sigma):
	'''
	r - size (d,) residuals, = x - mu
	sigma - size (d, d)
	'''
	d = r.size
	r = np.atleast_2d(r)
	top = np.exp(-1./2.* r @ np.linalg.inv(sigma) @ r.T)
	bottom = np.sqrt((2*np.pi)^d * np.linalg.det(sigma))
	return top/bottom

def em(x, pi0, mu0, sigma0, converge_threshold=0.1):
	'''
	Do expectation maximization for a mixture of m gaussians
	Following https://www.lri.fr/~sebag/COURS/mix_gauss.pdf

	Parameters
	----------
	x - [array] shape (n, d) the data where n is the
	    number of data points, d is the dimension of data

	pi0 - [array] shape (m,)
	mu0 - [array] shape (m, d) 
	sigma0 - [array] shape (m, d, d)
	    the initial parameters for mixture of gaussians:
	        sum_m(pi0_m * N(mu0_m, sigma0_m))

	converge_threshold - terminate when all parameters do
	    not update by more than this amount
	'''
	N = len(x)
	d = x.shape[1]
	M = len(pi0)
	while True:
		Ez = np.zeros([N, M])
		R = np.zeros([N, M, d])
		for i in range(N):
			pz = np.zeros(M) # p(x_i | z_im = 1; theta)
			for m in range(M):
				R[i, m] = x[i] - mu[m]
				pz[m] = multivariate_gaussian(R[i, m], sigma[m])
			for m in range(M): Ez[i, m] = pz[m] * pi0[m] / np.sum(pz * pi0)
		pi_new = np.zeros(M)
		mu_new = np.zeros([M, d])
		sigma_new = np.zeros([M, d, d])
		for m in range(M):
			pi_new[m] = np.sum(Ez[:, m]) / N
			mu_new[m] = np.sum(Ez[:, [m]] * x, axis=0) / np.sum(Ez[:, [m]])
			sigma_new[m] = np.sum(np.tile(np.atleast_3d(Ez[:, [m]]),[d,d])\
			                   * np.array([np.atleast_2d(r).T @ np.atleast_2d(r) for r in R[:, m, :]])) / np.sum(Ez[:, [m]])
		convergent = np.abs(np.mean(pi_new) - np.mean(pi0)) < converge_threshold\
		         and np.abs(np.mean(mu_new) - np.mean(mu0)) < converge_threshold\
		         and np.abs(np.mean(sigma_new) - np.mean(sigma0)) < converge_threshold
		pi0 = pi_new
		mu0 = mu_new
		sigma0 = sigma_new
		if convergent: break
	return pi0, mu0, sigma0
