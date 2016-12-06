import matplotlib.pyplot as plt
import numpy as np
from filters import NanAndCloseTo1Filter
from peakutils_wrapper import BaselineCorrection

from datasets.parse_cell_profiler_output import DataReaderAndParser
from transformations import TransformationPipeline, ClearNans,Thresholding
from transformations.tisean_wrapper import TiseanTransformation

condition_ranges_longtime = {1:"0 pg EGF",10:"10 pg EGF",20:"50 pg EGF",30:"200 pg EGF"}

threshold = 0.009

dataset = DataReaderAndParser(condition_ranges_longtime,nframes=257,file="""results 11_08_2016\\A1_Longtime_Cells.csv""").read()

tp_ = TransformationPipeline([ClearNans(),TiseanTransformation('sav_gol -n15,15 -p3'),BaselineCorrection(7),Thresholding(threshold=threshold)])
filter_ = NanAndCloseTo1Filter()

subplot_idx = {0:2,1:3,2:1,3:4}
	
plt.figure(figsize=(10,10))
for condition_idx,scd in enumerate(sorted(dataset._scd)):#iterate over conditions
	freqs = []
	ampl = []
	cells_peaks = []
	for scmd in scd._scmd:#iterate over cells
		if filter_.filter(scmd.get_time_series(),scmd._position,scmd._cell_idx):
			continue
		ts = tp_.transform(scmd.get_time_series())
		ts = np.array(ts)
		start_i = -1
		for i in range(len(ts)):
			if ts[i] > 0:
				if start_i < 0:
					start_i = i
			if ts[i] <= 0:
				if start_i > -1:
					if i-start_i-1 > 3:
						tuple_ = (start_i,i-1)
						cells_peaks.append(tuple_)
					start_i = -1
	durations = [(e[1]-e[0])/6.0 for e in cells_peaks]
	weights = np.ones_like(durations)/float(len(durations))
	plt.subplot(2,2,subplot_idx[condition_idx])
	plt.hist(durations,weights=weights)
	plt.xlabel('Pulse Duration [hours]')
	plt.ylabel('Pulse fraction')
	plt.ylim([0,0.3])
	plt.title(scd._condition_label+" (#pulses="+str(len(durations))+")")
plt.savefig('C:\\Users\\gajduk\\Desktop\\figs\\peak_duration.png')
plt.close()


