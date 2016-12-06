import matplotlib.pyplot as plt
import numpy as np
import peakutils
from filters import NanAndCloseTo1Filter
from peakutils_wrapper import BaselineCorrection

from datasets.parse_cell_profiler_output import DataReaderAndParser
from transformations import TransformationPipeline, ClearNans
from transformations.tisean_wrapper import TiseanTransformation

condition_ranges_longtime = {1:"0 pg EGF",10:"10 pg EGF",20:"50 pg EGF",30:"200 pg EGF"}

dataset = DataReaderAndParser(condition_ranges_longtime,nframes=257,file="""results 11_08_2016\\A1_Longtime_Cells.csv""").read()

tp_ = TransformationPipeline([ClearNans(),TiseanTransformation('sav_gol -n15,15 -p3'),BaselineCorrection(7)])
filter_ = NanAndCloseTo1Filter()

plt.figure(figsize=(10,10))

for condition_idx,scd in enumerate(dataset._scd):#iterate over conditions
	freqs = []
	ampl = []

	ampl_all = []
	dur_all = []
	for scmd in scd._scmd:#iterate over cells
		if filter_.filter(scmd.get_time_series(),scmd._position,scmd._cell_idx):
			continue
		ts = tp_.transform(scmd.get_time_series())
		ts = np.array(ts)
		indexes = peakutils.indexes(ts, thres=0.4, min_dist=18)
		for i in range(len(indexes)-1):
			freqs.append((indexes[i+1]-indexes[i])/6.0)
			ampl.append((ts[indexes[i+1]]+ts[indexes[i]])/2.0)

		for i in range(len(indexes)):
			peak_idx = indexes[i]
			ampl_all.append(ts[peak_idx])
			k = peak_idx
			while k >= 0:
				if ts[k] < 0.02:
					break
				k -= 1
			l = peak_idx-k

			k = peak_idx
			while k < len(ts):
				if ts[k] < 0.02:
					break
				k += 1
			l += k-peak_idx
			dur_all.append(l/6.0)


	plt.subplot(2,2,subplot_idx[condition_idx])
	plt.scatter(freqs,ampl)
	plt.xlabel('ISI [hours]')
	plt.ylabel('Pulse Amplitude (Avg.)')
	plt.ylim([0.0,0.4])
	plt.grid()
	plt.title(scd._condition_label)
	plt.tight_layout()

plt.savefig('C:\\Users\\gajduk\\Desktop\\figs\\scatter.png',dpi=600)
