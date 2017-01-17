import matplotlib.pylab as plt
from filters import GoodCellFilter,ManualFilter,MultipleFilters

from datasets.datasets import getDataset
from plotter import SingleCell3DPlotter
from transformations.transformations import TransformationPipeline, ManualBoundaryClipping
from transformations.tisean_wrapper import TiseanTransformation,embeding_dimension


def calculate_embeding_dimensions():
	dataset = getDataset("hke3_batch1")
	for scd in dataset._scd:
		print scd._condition_label+" "+str(len(scd._scmd))

	tp = TransformationPipeline([ManualBoundaryClipping()])
	f = MultipleFilters([ManualFilter()])
	plt.figure(figsize=(10,10))
	subplot_idx = 1
	for scd in dataset._scd:
		plt.subplot(2,2,subplot_idx)
		subplot_idx = subplot_idx+1
		combined = {1:[],2:[],3:[],4:[],5:[],6:[]}
		for scmd in scd._scmd:#iterate over cells
			position = scmd._position
			cell_idx = scmd._cell_idx
			ts = scmd.get_time_series()
			if f.filter(ts,position,cell_idx):
				continue
			ts = tp.transform(scmd.get_time_series())
			temp = embeding_dimension(ts)
			for e in temp:
				combined[e].append(temp[e])
		to_plot = []
		for dim in [1,2,3,4,5,6]:
			to_plot.append(combined[dim])
		plt.violinplot(to_plot,showmedians=True)
		plt.xlabel('Embeding dimension')
		plt.ylabel('Fraction of false nearest neighbors')
		plt.xticks([1,2,3,4,5,6],["1","2","3","4","5","6"])
		plt.title(scd._condition_label+" (#"+str(len(scd._scmd))+")")
		plt.grid()
	plt.savefig("embeding hke3.png",dpi=300)




def plot_embeding_dimensions():
	dataset = getDataset("batch2")
	for scd in dataset._scd:
		print scd._condition_label+" "+str(len(scd._scmd))
	#tp = TransformationPipeline([ClearNans(),TiseanTransformation('sav_gol -n15,15 -p3'),BaselineCorrection(5)])
	filter_ = GoodCellFilter()
	plotter = SingleCell3DPlotter(dataset,None,filter_)
	plotter.plot()

if __name__ == "__main__":
	calculate_embeding_dimensions()