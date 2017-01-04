import numpy as np

from transformations.transformations import removeNans


def get_rp(ts, de=0.1):
	ts = removeNans(ts)[0]
	n = len(ts)
	res = np.zeros((n, n))
	for i in range(n):
		for k in range(n):
			if de > (ts[i] - ts[k])**2:
				res[i, k] = 1
	return res


def get_diagonal_lines(rp):
	res = []
	n = rp.shape[0]
	for diag in range(n * 2 + 1):
		j = 0
		while j < n and 0 <= diag - j < n:
			start_j = j
			while j < n and 0 <= diag - j < n and rp[j, diag - j] == 1:
				j = j + 1
			v = j - start_j
			if v >= 1:
				res.append(v)
			j = j + 1
	return res


def get_vertical_lines(rp):
	res = []
	n = rp.shape[0]
	for i in range(n):
		j = 0
		while j < n:
			start_j = j
			while j < n and rp[j, i] == 1:
				j = j + 1
			v = j - start_j
			if v >= 1:
				res.append(v)
			j = j + 1
	return res


def getpv(vs, n, min):
	pv = np.zeros((n * 2 + 1, 1))
	for v in vs:
		try:
			pv[v] += 1
		except:
			pass
	total = np.sum(pv[min:])
	for v in range(n * 2 + 1):
		if v < min:
			pv[v] = 0
		else:
			pv[v] /= total
	return pv


def lam(rp, v_min):
	n = rp.shape[0]
	vs = get_vertical_lines(rp)
	pvmin = getpv(vs, n, v_min)
	pv = getpv(vs, n, 0)
	lam_top = np.sum([pvmin[v] * v for v in range(2 * n + 1)])
	lam_bot = np.sum([pv[v] * v for v in range(2 * n + 1)])
	return lam_top * 1.0 / lam_bot


def tt(rp, v_min):
	n = rp.shape[0]
	vs = get_vertical_lines(rp)
	pv = getpv(vs, n, 0)
	tt_top = np.sum([pv[v] * v for v in range(v_min, 2 * n + 1)])
	tt_bot = np.sum([pv[v] for v in range(v_min, 2 * n + 1)])
	return tt_top * 1.0 / tt_bot


def test_lam():
	n = 500
	x = np.random.rand(n, n)
	x[x > .3] = 1
	x[x < .3] = 0
	vs = get_vertical_lines(x)
	print tt(x, 2)

	t = np.linspace(0, 20, n)
	y = np.sin(t) + np.sin(t * 3)
	de = .5
	n = len(y)
	im = np.zeros((n, n))
	for i in range(n):
		for k in range(n):
			if de > np.abs(y[i] - y[k]):
				im[i, k] = 1

	print tt(im, 2)
	from filters import mchaingen
	xx = np.array(mchaingen(n=n)) + np.random.randn(n) * 0.25
	imxx = np.zeros((n, n))
	de = .7
	for i in range(n):
		for k in range(n):
			if de > np.abs(xx[i] - xx[k]):
				imxx[i, k] = 1

	print tt(imxx, 2)

def rr(rp):
	return np.sum(np.sum(rp))*1.0/(rp.shape[0]*rp.shape[1])

if __name__ == "__main__":
	test_lam()

statistics = {'LAM': lam}
