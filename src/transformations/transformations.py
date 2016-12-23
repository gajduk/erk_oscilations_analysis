import numpy as np
from scipy.signal import savgol_filter

from utils import get_manual_boundaries


def removeNans(ts):
	temp = []
	temp_idxs = []
	last_non_nan_idx = -1
	i = 0
	max_size_nans = 4
	while i < len(ts):
		if np.isnan(ts[i]):
			while i < len(ts) and np.isnan(ts[i]):
				i = i + 1
			if i == len(ts):
				break
			else:
				if last_non_nan_idx >= 0 and i - last_non_nan_idx <= max_size_nans:
					l = i - last_non_nan_idx
					dv = ts[i] - ts[last_non_nan_idx]
					step = dv * 1.0 / l
					for k in range(1, l):
						temp_idxs.append(last_non_nan_idx + k)
						temp.append(ts[last_non_nan_idx] + k * step)
		temp.append(ts[i])
		temp_idxs.append(i)
		last_non_nan_idx = i
		i = i + 1
	return temp, temp_idxs


def removeNansDecorator(transform):
	def inner(self, ts, pos):
		temp, temp_idxs = removeNans(ts)
		transformed = transform(self, temp)
		k = 0
		res = []
		for i in range(len(ts)):
			if i in temp_idxs and len(transformed) > k:
				res.append(transformed[k])
				k = k + 1
			else:
				res.append(float('NaN'))
		return res

	return inner


def testRemoveNans():
	@removeNansDecorator
	def sample_transform(self, ts):
		return [e for e in ts]

	print sample_transform(0, [1, 2, float('NaN'), 3, 4])
	print sample_transform(0, [float('NaN'), 2, float('NaN'), 3, 4])
	print sample_transform(0, [float('NaN'), 2, float('NaN'), 3, 4])
	print sample_transform(0, [1, float('NaN'), 2, float('NaN'), 3, 4])
	print sample_transform(0, [1, float('NaN'), float('NaN'), float('NaN'), 3, 4])
	print sample_transform(0, [1, float('NaN'), float('NaN'), float('NaN'), float('NaN'), 3, 4])

	print sample_transform(0, [1, float('NaN'), 2, float('NaN'), 3, 4, float('NaN')])
	print sample_transform(0, [1, float('NaN'), 2, float('NaN'), 3, 4, float('NaN'), float('NaN')])


if __name__ == "__main__":
	testRemoveNans()


def find_min_max(data):
	min_ = 100000
	max_ = 0
	for e in data:
		if np.isnan(e):
			continue
		if e < min_:
			min_ = e
		if e > max_:
			max_ = e
	return min_, max_


class SavGolFilter:
	def __init__(self, n=11, p=3):
		self.n = n
		self.p = p

	@removeNansDecorator
	def transform(self, ts, pos=None):
		return savgol_filter(ts, window_length=self.n, polyorder=self.p, mode='interp')

	def __str__(self):
		return "SavGol n " + str(self.n) + " p" + str(self.p)


def testSavGolFilter():
	import random
	f = SavGolFilter(n=3, p=2)
	ts = [float('NaN') if random.random() > 0.5 else e for e in np.random.rand(100)]
	print len(ts), ts
	print len(f.transform(ts)), f.transform(ts)


if __name__ == "__main__":
	testSavGolFilter()


class TransformationPipeline:
	_transformations = -1

	def __init__(self, transformations):
		self._transformations = transformations

	def transform(self, data, pos=None):
		res = data
		for transformation in self._transformations:
			res = transformation.transform(res,pos)
		return res

	def __str__(self):
		return "__".join([str(e) for e in self._transformations])


class MovingAverage:
	_window_size = -1

	def __init__(self, window_size=5):
		self._window_size = window_size

	def transform(self, interval, pos=None):
		window = np.ones(int(self._window_size)) / float(self._window_size)
		return np.convolve(interval, window, 'same')

	def __str__(self):
		return "Moving avg (" + str(self._window_size) + ")"


class Thresholding:
	_threshold = -1

	def __init__(self, threshold=0.01):
		self._threshold = threshold

	@removeNansDecorator
	def transform(self, ts, pos=None):
		return [1 if e > self._threshold else 0 for e in ts]

	def __str__(self):
		return "Threshold at (" + str(self._threshold) + ")"


class ManualBoundaryClipping:
	def __init__(self):
		self._boundaries = get_manual_boundaries()

	def transform(self, ts, pos=None):
		res = []
		start, end = 0,299
		if pos in self._boundaries:
			start, end = self._boundaries[pos]
		for i, e in enumerate(ts):
			if start <= i <= end:
				res.append(e)
			else:
				res.append(float('NaN'))
		return res

	def __str__(self):
		return "Manual"


class Difference:
	_step = -1

	def __init__(self, step=3):
		self._step = step

	@removeNansDecorator
	def transform(self, ts, pos=None):
		res = []
		for k in range(len(ts) - self._step):
			if np.isnan(ts[k]) or np.isnan(ts[k + self._step]):
				res.append(float('NaN'))
			else:
				res.append(ts[k + self._step] - ts[k])
		for k in range(self._step):
			res.append(float('NaN'))
		return res

	def __str__(self):
		return "Difference (" + str(self._step) + ")"


class NormalizedByMin:
	def __init__(self):
		pass

	@removeNansDecorator
	def transform(self, ts, pos=None):
		min_, max_ = find_min_max(ts)
		return [e / min_ for e in ts]

	def __str__(self):
		return "Normalized by Min"


class NormalizedByMax:
	def __init__(self):
		pass

	@removeNansDecorator
	def transform(self, ts, pos=None):
		min_, max_ = find_min_max(ts)
		return [e / max_ for e in ts]

	def __str__(self):
		return "Normalized by Max"


class FoldChange:
	def __init__(self):
		pass

	@removeNansDecorator
	def transform(self, ts, pos=None):
		first_ = -1
		for e in ts:
			if not np.isnan(e):
				first_ = e
				break
		return [e / first_ for e in ts]

	def __str__(self):
		return "FoldChange"


class Fourier:
	def __init__(self):
		pass

	def transform(self, ts, pos=None):
		return np.fft.fft(ts)

	def __str__(self):
		return "Fourier"
