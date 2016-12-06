import matplotlib.pyplot as plt
import numpy as np
from filters import NanAndCloseTo1Filter
from peakutils_wrapper import BaselineCorrection

from datasets.parse_cell_profiler_output import DataReaderAndParser
from transformations import TransformationPipeline, ClearNans,Thresholding
from transformations.tisean_wrapper import TiseanTransformation


def order_j_aneta_paper():
	condition_ranges_longtime = {1:"0 pg EGF",10:"10 pg EGF",20:"50 pg EGF",30:"200 pg EGF"}

	threshold = 0.009

	dataset = DataReaderAndParser(condition_ranges_longtime,nframes=257,file="""results 11_08_2016\\A1_Longtime_Cells.csv""").read()

	tp_ = TransformationPipeline([ClearNans(),TiseanTransformation('sav_gol -n15,15 -p3'),BaselineCorrection(7),Thresholding(threshold=threshold)])
	filter_ = NanAndCloseTo1Filter()

	subplot_idx = {0:2,1:3,2:1,3:4}
		
	x = [0,1,2,3]
	y = [0,0,0,0]
	for condition_idx,scd in enumerate(dataset._scd):#iterate over conditions
		jumps = []
		for scmd in scd._scmd:#iterate over cells
			if filter_.filter(scmd.get_time_series(),scmd._position,scmd._cell_idx):
				continue
			ts = tp_.transform(scmd.get_time_series())
			ts = np.array(ts)
			start_i = -1
			count = 0
			for i in range(1,len(ts)):
				if ts[i] > 0:
					if ts[i-1] <= 0:
						count += 1
			jumps.append(count)
		j = sum(jumps)*1.0/(len(scd._scmd)*257)
		y[subplot_idx[condition_idx]-1] = j


	plt.figure(figsize=(4,4))
	plt.plot(x,y,'o')
	plt.xticks([0,1,2,3],['0','10','50','200'])
	plt.xlabel('pg EGF')
	plt.ylabel('j')
	plt.xlim([-0.5,3.5])
	plt.tight_layout()
	plt.grid()
	#plt.title(scd._condition_label+" (#pulses="+str(len(durations))+")")
	plt.savefig('C:\\Users\\gajduk\\Desktop\\figs\\j.png')
	plt.close()

def order_f_aneta_paper():
	condition_ranges_longtime = {1:"0 pg EGF",10:"10 pg EGF",20:"50 pg EGF",30:"200 pg EGF"}

	threshold = 0.009
	nframes = 257
	dataset = DataReaderAndParser(condition_ranges_longtime,nframes=nframes,file="""results 11_08_2016\\A1_Longtime_Cells.csv""").read()

	tp_ = TransformationPipeline([ClearNans(),TiseanTransformation('sav_gol -n15,15 -p3'),BaselineCorrection(7),Thresholding(threshold=threshold)])
	filter_ = NanAndCloseTo1Filter()

	subplot_idx = {0:2,1:3,2:1,3:4}
		
	x = [0,1,2,3]
	y = [0,0,0,0]
	for condition_idx,scd in enumerate(dataset._scd):#iterate over conditions
		counts = [0 for i in range(nframes)]
		for scmd in scd._scmd:#iterate over cells
			if filter_.filter(scmd.get_time_series(),scmd._position,scmd._cell_idx):
				continue
			ts = tp_.transform(scmd.get_time_series())
			ts = np.array(ts)
			start_i = -1
			count = 0
			for i in range(len(ts)):
				if ts[i] > 0:
					counts[i] += 1
		f = sum([counts[i]*1.0/len(scd._scmd) for i in range(nframes)])*1.0/nframes
		y[subplot_idx[condition_idx]-1] = f


	plt.figure(figsize=(4,4))
	plt.plot(x,y,'o')
	plt.xticks([0,1,2,3],['0','10','50','200'])
	plt.xlabel('pg EGF')
	plt.ylabel('f')
	plt.xlim([-0.5,3.5])
	plt.tight_layout()
	plt.grid()
	#plt.title(scd._condition_label+" (#pulses="+str(len(durations))+")")
	plt.savefig('C:\\Users\\gajduk\\Desktop\\figs\\f.png')
	plt.close()



order_f_aneta_paper()