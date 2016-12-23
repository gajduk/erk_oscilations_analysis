import numpy as np
from statsmodels.tsa.stattools import adfuller

from transformations.transformations import removeNans
from utils import get_manual_boundaries

good_cells_longtime = {(1, 1), (1, 2), (10, 1), (4, 1), (4, 2), (4, 4), (4, 5), (6, 1), (6, 2), (6, 5), (7, 1), (7, 2),
                       (7, 3), (7, 4), (7, 5), (8, 1), (8, 2), (9, 3), (12, 1), (12, 2), (13, 1), (13, 4), (15, 1),
                       (15, 2), (15, 3), (15, 4), (16, 1), (16, 2), (16, 3), (16, 4), (16, 5), (17, 1), (17, 2),
                       (17, 3), (17, 4), (18, 1), (19, 1), (19, 2), (19, 3), (20, 1), (20, 2), (31, 1), (31, 2),
                       (33, 1), (33, 2), (33, 3), (34, 1), (34, 2), (40, 2), (21, 1), (21, 2), (23, 1), (23, 2),
                       (23, 3), (23, 4), (23, 5), (24, 1), (24, 2), (24, 3), (25, 2), (25, 3), (25, 4), (30, 1),
                       (30, 2)}


class ManualFilter:
	def __init__(self):
		self._boundaries = get_manual_boundaries()

	def filter(self, ts, position, cell_idx):
		pos = (position, cell_idx)
		if pos in self._boundaries:
			return False
		return True

	def __str__(self):
		return "Manual"

class NoFilter:
	def __init__(self):
		pass

	def filter(self, ts, position, cell_idx):
		return False

	def __str__(self):
		return "NoFilter"


class Close_to_1_Fitler:
	def __init__(self):
		pass

	def filter(self, ts, position, cell_idx):
		count = 0
		for e in ts:
			if 1.0 - e > .1:
				count += 1
		return count <= 2

	def __str__(self):
		return "CloseTo1"


class GoodCellFilter:
	def __init__(self, good_cells=good_cells_longtime):
		self._good_cells = good_cells

	def filter(self, ts, position, cell_idx):
		if (position, cell_idx) in self._good_cells:
			return False
		return True

	def __str__(self):
		return "GoodCells"


class NanAndCloseTo1Filter:
	def __init__(self, good_percent=0.6):
		self._good_percent = good_percent

	def filter(self, ts, position, cell_idx):
		count_nan, count_1, count_good = 0, 0, 0
		for e in ts:
			if np.isnan(e):
				count_nan += 1
			elif 1.0 - e < .05:
				count_1 += 1
			else:
				count_good += 1
		return count_good * 1.0 / len(ts) < self._good_percent

	def __str__(self):
		return "NanAndCloseTo1 " + str(self._good_percent)


class MinConsecutiveLengthFilter:
	def __init__(self, l=50):
		self.l = l
		self.bad_positions = {('012', 8), ('012', 7), ('009', 1), ('023', 0), ('028', 1), \
		                      ('029', 0), ('035', 3), ('037', 0), ('041', 2), ('041', 4), ('052', 0), ('054', 0),
		                      ('054', 2), \
		                      ('058', 3), ('058', 5), ('058', 10), ('063', 2), ('063', 4), ('064', 6), ('063', 3),
		                      ('065', 7), ('059', 2), \
		                      ('037', 4)}

	def filter(self, ts, position, cell_idx):
		i = 0
		ll = 0
		if position == "060" or position == "052":
			return True
		if (position, cell_idx) in self.bad_positions:
			return True

		while i < len(ts):
			while i < len(ts) and not np.isnan(ts[i]):
				ll += 1
				i += 1
			if ll > self.l:
				return False
			i += 1
			ll = 0
		return True

	def __str__(self):
		return "MinLength " + str(self.l)


class AdFuller:
	def __init__(self):
		pass

	def filter(self, ts, position=None, cell_idx=None):
		ts, ts_idx = removeNans(ts)
		pvalue = adfuller(ts, regression='c')[1]
		print pvalue, ts
		if pvalue < .05:
			return False
		return True

	def __str__(self):
		return "AdFuller c"


class MultipleFilters:
	def __init__(self, filters):
		self.filters = [e for e in filters]

	def filter(self, ts, position, cell_idx):
		for f in self.filters:
			if f.filter(ts, position, cell_idx):
				return True
		return False

	def __str__(self):
		return " ".join(str(e) for e in self.filters)


def testMultipleFilters():
	from datasets.datasets import getDataset
	from plotter import SingleCellPlotter
	from transformations.transformations import TransformationPipeline
	dataset = getDataset("hke3_batch1")
	tp = TransformationPipeline([])
	filter = MultipleFilters([MinConsecutiveLengthFilter(150), AdFuller()])
	plotter = SingleCellPlotter(dataset, tp, filter, ylim=[0.6, 1.2])
	plotter.plot()


def testadfuller():
	import matplotlib.pylab as plt
	plt.figure(figsize=(14, 20))
	sigmas = [1, 2, 3, 5, 7, 9]
	for i in range(1, 7):
		sigma = sigmas[i - 1]
		x_stationary = np.random.randn(300) * sigma
		x_lintrend = np.random.randn(300) * sigma + np.linspace(0, 10, 300)
		x_nonlintrend = np.random.randn(300) * sigma + np.sqrt(np.linspace(0, 100, 300))
		plt.subplot(3, 2, i)
		s1, p1, _, _, _, _ = adfuller(x_stationary, regression='nc')
		s2, p2, _, _, _, _ = adfuller(x_lintrend, regression='nc')
		s3, p3, _, _, _, _ = adfuller(x_nonlintrend, regression='nc')
		plt.plot(x_stationary, color='blue', label='Stationary $s={0:.1f}$ $p={1:0.3f}$'.format(s1, p1))
		plt.plot(x_lintrend, color='red', label='Linear trend $s={0:.1f}$ $p={1:0.3f}$'.format(s2, p2))
		plt.plot(x_nonlintrend, color='green', label='Non-Linear trend $s={0:.1f}$ $p={1:0.3f}$'.format(s3, p3))
		plt.legend(loc='upper left')
		plt.xlabel('$t$')
		plt.ylabel('$y$')
		plt.title('$\sigma = {0:2.2f}$'.format(sigma))
		plt.grid()
	plt.savefig('temp.png', dpi=300)


def recurenceplot(ts, de):
	import matplotlib.pylab as plt
	n = len(ts)
	im = np.zeros((n, n))
	for i in range(n):
		for k in range(n):
			if de > np.abs(ts[i] - ts[k]):
				im[i, k] = 1
	plt.imshow(im, cmap='gray')


def mchaingen(n=100, p=[[0.99, 0.01], [0.02, 0.98]]):
	import random
	res = []
	x = 0
	for i in range(n):
		res.append(x)
		if random.random() < p[x][0]:
			x = 0
		else:
			x = 1
	return res


def test_mchaingen():
	import matplotlib.pylab as plt
	x = mchaingen()
	plt.figure(figsize=(30, 12))

	plt.subplot(2, 6, 2)
	xx = np.array(x) + np.random.randn(500) * 0.25
	plt.plot(xx)
	plt.subplot(2, 6, 8)
	recurenceplot(xx, .1)

	plt.subplot(2, 6, 3)
	xxx = np.array(x) + np.random.randn(500) * 0.5
	plt.plot(xxx)
	plt.subplot(2, 6, 9)
	recurenceplot(xxx, .2)

	plt.subplot(2, 6, 1)
	plt.plot(x)
	plt.ylim([-.1, 1.1])
	plt.subplot(2, 6, 7)
	recurenceplot(np.array(x), .2)

	sigma = 1
	plt.subplot(2, 6, 4)
	x_stationary = np.random.randn(500) * sigma
	plt.plot(x_stationary)
	plt.subplot(2, 6, 10)
	recurenceplot(x_stationary, .2)

	plt.subplot(2, 6, 5)
	x_lintrend = np.random.randn(500) * sigma + np.linspace(0, 10, 500)
	plt.plot(x_lintrend)
	plt.subplot(2, 6, 11)
	recurenceplot(x_lintrend, 2)

	plt.subplot(2, 6, 6)
	x_nonlintrend = np.random.randn(500) * sigma + np.sqrt(np.linspace(0, 100, 500))
	plt.plot(x_nonlintrend)
	plt.subplot(2, 6, 12)
	recurenceplot(x_nonlintrend, 2)

	plt.savefig('asd.png')


def testrecurenceplot():
	import matplotlib.pylab as plt
	plt.figure(figsize=(14, 20))
	sigma = 1
	de = .0001
	x_stationary = np.random.randn(300) * sigma
	x_lintrend = np.random.randn(300) * sigma + np.linspace(0, 10, 300)
	x_nonlintrend = np.random.randn(300) * sigma + np.sqrt(np.linspace(0, 100, 300))
	plt.subplot(3, 1, 1)
	recurenceplot(x_stationary, de)
	plt.subplot(3, 1, 2)
	recurenceplot(x_lintrend, de)
	plt.subplot(3, 1, 3)
	recurenceplot(x_nonlintrend, de)
	plt.savefig('temp.png', dpi=300)


if __name__ == "__main__":
	test_mchaingen()
