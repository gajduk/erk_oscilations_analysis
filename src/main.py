from filters import NanAndCloseTo1Filter,NoFilter
from transformations.peakutils_wrapper import BaselineCorrection,PeakMarker,SpecialTransformForShowcase
from datasets.datasets import getDataset
from plotter import SingleCellPlotter,CombinedImshowPlotter,RecurrenceStatScatter, ShowcaseCellPlotter
from transformations.transformations import TransformationPipeline, ManualBoundaryClipping, SubtractMovingAverage, NormalizedByMax, SavGolFilter, Difference, Thresholding
from transformations.tisean_wrapper import TiseanTransformation
from filters import MinConsecutiveLengthFilter,ManualFilter,MultipleFilters,GoodCellFilter


dataset = getDataset("hke3_batch1")

tp = TransformationPipeline([ManualBoundaryClipping(),SavGolFilter(),BaselineCorrection()])
f = MultipleFilters([NoFilter()])

#plot individual time series
SingleCellPlotter(dataset,tp,f,ylim=[-0.002, 0.05]).plot()

#plot the time series color coded
CombinedImshowPlotter(dataset,tp,f).plot()

#plot metrics from recurence plots
RecurrenceStatScatter(dataset,tp,f).plot()