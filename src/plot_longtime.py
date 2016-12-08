from filters import NanAndCloseTo1Filter,NoFilter
from transformations.peakutils_wrapper import BaselineCorrection,PeakMarker

from datasets.datasets import getDataset
from plotter import SingleCellPlotter,SingleConditionPlotter
from transformations.transformations import TransformationPipeline, ClearNans, NormalizedByMax, SavGolFilter, Difference
from transformations.tisean_wrapper import TiseanTransformation
from filters import MinConsecutiveLengthFilter

dataset = getDataset("hke3_batch1")
for scd in dataset._scd:
	print scd._condition_label+" "+str(len(scd._scmd))

# BaselineCorrection(5)
#plotter = SingleCellPlotter(dataset,TransformationPipeline([SavGolFilter(n=31,p=3)]),MinConsecutiveLengthFilter(150))
'''
plotter = SingleCellPlotter(dataset,TransformationPipeline([]),MinConsecutiveLengthFilter(150))
plotter.plot()
'''
tp_imshow = TransformationPipeline([SavGolFilter(n=19,p=3),BaselineCorrection(4),PeakMarker(thres=0.3,min_dist=8)])
imshow_plotter = SingleConditionPlotter(dataset,tp_imshow,MinConsecutiveLengthFilter(150))
imshow_plotter.plot()

#plotter = SingleCellPlotter(dataset,tp_imshow,MinConsecutiveLengthFilter(150))
#plotter.plot()
