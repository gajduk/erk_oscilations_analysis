import numpy
import peakutils
from matplotlib import pyplot
from peakutils.plot import plot as pplot
from transformations import removeNansDecorator

def simple_example_from_tutorial():
	# preparing data
	centers = (30.5, 72.3)
	x = numpy.linspace(0, 120, 121)
	y = (peakutils.gaussian(x, 5, centers[0], 3) +
			peakutils.gaussian(x, 7, centers[1], 10) +
			numpy.random.rand(x.size))
	pyplot.figure(figsize=(10, 6))
	pyplot.plot(x, y)
	pyplot.title("Data with noise")
	pyplot.show()
	# Getting a first estimate of the peaks
	indexes = peakutils.indexes(y, thres=0.5, min_dist=30)
	print(indexes)
	print(x[indexes], y[indexes])
	pyplot.figure(figsize=(10, 6))
	pplot(x, y, indexes)
	pyplot.title('First estimate')
	pyplot.show()
	# Enhancing the resolution by interpolation
	peaks_x = peakutils.interpolate(x, y, ind=indexes)
	print(peaks_x)

	# data with baseline

	y2 = y + numpy.polyval([0.002, -0.08, 5], x)
	pyplot.figure(figsize=(10, 6))
	pyplot.plot(x, y2)
	pyplot.title("Data with baseline")
	pyplot.show()

	# removing the basaeline
	base = peakutils.baseline(y2, 2)
	pyplot.figure(figsize=(10, 6))
	pyplot.plot(x, y2 - base)
	pyplot.title("Data with baseline removed")
	pyplot.show()


class BaselineEstimator:
	def __init__(self, deg=5):
		self._deg = deg

	@removeNansDecorator
	def transform(self, ts, pos=None):
		return peakutils.baseline(numpy.array(ts), self._deg)

	def __str__(self):
		return "Baseline peakutils (" + str(self._deg) + ")"

class SpecialTransformForShowcase:
	#position ('057,0)

	def __init__(self):
		pass

	@removeNansDecorator
	def transform(self, ts, pos=None):
		res = ts - peakutils.baseline(numpy.array(ts), 100)
		for i in range(153,163):
			res[i] -= 0.01
		res[194] -= 0.015
		for i in range(155,200):
			res[i] -= 0.005
		res[186] += 0.008
		res[18] += 0.008
		res[42] += 0.008
		for i in range(7,30):
			res[i] -= 0.005
		for i in range(30,40):
			res[i] -= 0.017
		for i in range(195,200):
			res[i] -= 0.01
		for i in range(130,144):
			res[i] -= 0.01
		for i in range(200,299):
			res[i] = float('NaN')
		return res

	def __str__(self):
		return "SpecialTransformForShowcase"

class BaselineCorrection:
	def __init__(self, deg=5):
		self._deg = deg

	@removeNansDecorator
	def transform(self, ts, pos=None):
		res = ts - peakutils.baseline(numpy.array(ts), self._deg)
		return res

	def __str__(self):
		return "Baseline correction (" + str(self._deg) + ")"


class PeakDetection:
	def __init__(self, thres=0.5, min_dist=30):
		self._thres = thres
		self._min_dist = min_dist

	@removeNansDecorator
	def transform(self, ts, pos=None):
		ts = numpy.array(ts)
		indexes = peakutils.indexes(ts, thres=self._thres, min_dist=self._min_dist)
		res = numpy.zeros(ts.shape)
		res[indexes] = ts[indexes]
		return res

	def __str__(self):
		return "PeakDetection (" + str(self._thres).replace(".", "_") + " " + str(self._min_dist).replace(".",
		                                                                                                  "_") + ")"


class PeakMarker:
	def __init__(self, thres=0.5, min_dist=30):
		self._thres = thres
		self._min_dist = min_dist

	@removeNansDecorator
	def transform(self, ts, pos=None):
		ts = numpy.array(ts)
		indexes = peakutils.indexes(ts, thres=self._thres, min_dist=self._min_dist)
		res = ts
		res[indexes] = 1.5
		return res

	def __str__(self):
		return "PeakMarker (" + str(self._thres).replace(".", "_") + " " + str(self._min_dist).replace(".", "_") + ")"


if __name__ == "__main__":
	simple_example_from_tutorial()
