
import numpy as np
import matplotlib.pylab as plt
from recurence_plot_quantifications import get_rp

def plot_rp(ts):
	xticks = [i * 6 * 2 for i in range(17)]
	xlabels = ['' if i % 4 > 0 else str(i * 2) for i in range(17)]
	rp = get_rp(ts,de = 0.2)
	plt.figure(figsize=(4, 4))
	plt.imshow(rp,cmap='gray',interpolation='none')
	plt.xlim([0, 200])
	plt.ylim([0, 200])
	plt.xticks(xticks,xlabels)
	plt.yticks(xticks,xlabels)
	plt.xlabel('Time [Hours]')
	plt.ylabel('Time [Hours]')
	plt.tight_layout()
	plt.savefig('asd.png', transparent=True, dpi=1200)
	plt.close()

def plot_random():
	x = np.random.randn(201)
	plot_rp(x)

def plot_oscilations():
	n = 200

	mask = np.zeros((n, n))
	for i in range(n):
		for t in np.linspace(-10,10,11):
			ni = int(i-t*20)
			for k in range(ni-10,ni+10):
				if 0 <= k < 200:
					mask[i,n-k-1] = 1
	res = np.ones((n, n))
	for i in range(n):
		for t in np.linspace(-10, 10, 6):
			ni = int(i - t * 20)
			for k in range(ni - 1, ni + 1):
				if 0 <= k < 200:
					res[i, k] = mask[i][k]

		for t in np.linspace(-8, 8, 5):
			ni = int(i - t * 20)
			for k in range(ni - 1, ni + 1):
				if 0 <= k < 200:
					res[i, k] = 0

	xticks = [i * 6 * 2 for i in range(17)]
	xlabels = ['' if i % 4 > 0 else str(i * 2) for i in range(17)]
	plt.figure(figsize=(4, 4))
	plt.imshow(res, cmap='gray', interpolation='none')
	plt.xlim([0, 200])
	plt.ylim([0, 200])
	plt.xticks(xticks, xlabels)
	plt.yticks(xticks, xlabels)
	plt.xlabel('Time [Hours]')
	plt.ylabel('Time [Hours]')
	plt.tight_layout()
	plt.savefig('asd.png', transparent=True, dpi=1200)
	plt.close()

if __name__ == "__main__":
	plot_oscilations()

