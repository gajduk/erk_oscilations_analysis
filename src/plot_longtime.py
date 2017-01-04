from filters import NanAndCloseTo1Filter,NoFilter
from transformations.peakutils_wrapper import BaselineCorrection,PeakMarker,SpecialTransformForShowcase

from datasets.datasets import getDataset
from plotter import SingleCellPlotter,CombinedImshowPlotter,RecurrenceStatScatter, ShowcaseCellPlotter
from transformations.transformations import TransformationPipeline, ManualBoundaryClipping, SubtractMovingAverage, NormalizedByMax, SavGolFilter, Difference, Thresholding
from transformations.tisean_wrapper import TiseanTransformation
from filters import MinConsecutiveLengthFilter,ManualFilter,MultipleFilters,GoodCellFilter
import numpy
import matplotlib.pylab as plt
from scipy.stats import anderson

dataset = getDataset("hke3_batch1")

tp = TransformationPipeline([ManualBoundaryClipping(),SpecialTransformForShowcase()])
f = MultipleFilters([ManualFilter(),GoodCellFilter([('057',0)])])

plotter = SingleCellPlotter(dataset,tp,f,ylim=[-0.002, 0.05])
plotter.plot()
