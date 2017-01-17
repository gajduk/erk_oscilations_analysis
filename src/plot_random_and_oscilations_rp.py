
import numpy as np
import matplotlib.pylab as plt
from recurence_plot_quantifications import get_rp

def plot_rp(ts):
	xticks = [i * 6 * 4 for i in range(17)]
	xlabels = ['' if i % 4 > 0 else str(i * 2) for i in range(17)]
	rp = get_rp(ts,de = 0.05)
	plt.figure(figsize=(3, 3))
	plt.imshow(1-rp,cmap='gray',interpolation='none')
	plt.xlim([0, 400])
	plt.ylim([0, 400])
	plt.xticks(xticks,xlabels)
	plt.yticks(xticks,xlabels)
	plt.xlabel('Time [Hours]',fontweight='bold')
	plt.ylabel('Time [Hours]',fontweight='bold')
	plt.tick_params(
	    axis='x',          # changes apply to the x-axis
	    which='both',      # both major and minor ticks are affected
	    bottom='off',      # ticks along the bottom edge are off
	    top='off'
	    ) # labels along the bottom edge are off

	plt.tick_params(
		axis='y',  # changes apply to the x-axis
		which='both',  # both major and minor ticks are affected
		left='off',  # ticks along the bottom edge are off
		right='off'
	)  # labels along the bottom edge are off
	plt.tight_layout()
	plt.savefig('asd.png', transparent=True, dpi=1200)
	plt.close()

def plot_random():
	x = np.random.randn(401)
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
	plt.figure(figsize=(3, 3))
	plt.imshow(res, cmap='gray', interpolation='none')
	plt.xlim([0, 200])
	plt.ylim([0, 200])
	plt.xticks(xticks, xlabels)
	plt.yticks(xticks, xlabels)
	plt.xlabel('Time [Hours]',fontweight='bold')
	plt.ylabel('Time [Hours]',fontweight='bold')
	plt.tight_layout()
	plt.savefig('asd.png', transparent=True, dpi=1200)
	plt.close()

if __name__ == "__main__":
	plot_random()

