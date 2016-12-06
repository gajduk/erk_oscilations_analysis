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

for scd in dataset._scd:#iterate over conditions
	freqs = []
	ampl = []
	for scmd in scd._scmd:#iterate over cells
		if filter_.filter(scmd.get_time_series(),scmd._position,scmd._cell_idx):
			continue
		ts = tp_.transform(scmd.get_time_series())
		ts = np.array(ts)
		indexes = peakutils.indexes(ts, thres=0.4, min_dist=18)
		for i in range(len(indexes)-1):
			freqs.append((indexes[i+1]-indexes[i])/6.0)
		if len(indexes)>0:
			freqs.append(indexes[0]/6.0)
			freqs.append((257-indexes[-1])/6.0)

		ampl.extend([e for e in ts[indexes]])
	plt.figure()
	weights = np.ones_like(freqs)/float(len(freqs))
	plt.hist(freqs,weights=weights)
	print scd._condition_label,len(freqs)
	plt.xlabel('Pulse Period [hours]')
	plt.ylabel('Pulse fraction')
	plt.ylim([0,0.5])
	plt.title(scd._condition_label)
	plt.savefig('C:\\Users\\gajduk\\Desktop\\figs\\freq_'+scd._condition_label+'.png')
	plt.close()

	plt.figure()
	weights = np.ones_like(ampl)/float(len(ampl))
	plt.hist(ampl,weights=weights)
	plt.xlabel('Pulse Amplitude')
	plt.ylabel('Pulse fraction')
	plt.title(scd._condition_label)
	plt.savefig('C:\\Users\\gajduk\\Desktop\\figs\\ampl_'+scd._condition_label+'.png')
	plt.close()

