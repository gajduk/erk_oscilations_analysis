from filters import NanAndCloseTo1Filter,NoFilter
from transformations.peakutils_wrapper import BaselineCorrection,PeakMarker

from datasets.datasets import getDataset
from plotter import SingleCellPlotter,CombinedImshowPlotter,Plotter,RecurrenceStatScatter
from transformations.transformations import TransformationPipeline, ManualBoundaryClipping, NormalizedByMax, SavGolFilter, Difference, PeakDetection
from transformations.tisean_wrapper import TiseanTransformation
from filters import MinConsecutiveLengthFilter,ManualFilter
import numpy as np
import matplotlib.pylab as plt
from scipy.stats import anderson


class ISIScatter(Plotter):
	def __init__(self, dataset, transformation, filter_, threshold=0.6, min_dist=3):
		Plotter.__init__(self, dataset, transformation, filter_)
		self.peaks_detection = PeakDetection(threshold, min_dist)

	def plot(self):
		xs, ys = [], []
		for scd_idx, scd in enumerate(self._dataset._scd):  # iterate over conditions
			for idx, scmd in enumerate(scd._scmd):  # iterate over cells
				if self.is_cell_filtered(scmd):
					continue
				ts = self.get_time_series(scmd)
				ts = self.peaks_detection.transform(ts, None)
				indexes = np.where(np.array(ts) > 0)[0]
				for i in range(len(indexes) - 1):
					y = indexes[i + 1] - indexes[i]
					if y > 60:
						continue
					xs.append((indexes[i + 1] - indexes[i]) / 2 + indexes[i])
					ys.append(y)
		plt.figure(figsize=(12, 6))
		plt.scatter(xs, ys, marker='+')
		plt.xlabel('Frame [' + str(self._dataset._frame_length_in_minutes) + ' min]')
		plt.ylabel('ISI')
		plt.xlim([0, self._dataset._nframes])
		plt.ylim([0, 65])
		plt.tight_layout()
		plt.savefig(self._folder + "ISIScatter.png", dpi=300, transparent=True)
		plt.close()

		from scipy.stats import anderson, expon
		plt.figure(figsize=(6, 6))
		plt.hist(ys, bins=30,label="data $S_{{Anderson}} = {0:.2f}$".format(anderson(ys)[0]),normed ='True')
		loc, scale = expon.fit(ys)
		exp_fit = expon(loc=loc,scale=scale)
		x = np.linspace(4,60,100)

		plt.plot(x+1, exp_fit.pdf(x), 'k-', lw=2, label='exponential fit')
		plt.xlabel('ISI [10 mins]')
		plt.ylabel('Count (norm.)')
		plt.legend()
		plt.savefig(self._folder + "ISI hist.png", dpi=300, transparent=True)
		plt.close()

dataset = getDataset("hke3_batch1")

tp = TransformationPipeline([ManualBoundaryClipping(),BaselineCorrection(5)])
f = ManualFilter()

plotter = ISIScatter(dataset,tp,f)
plotter.plot()
