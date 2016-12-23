from filters import NanAndCloseTo1Filter,NoFilter
from transformations.peakutils_wrapper import BaselineCorrection,PeakMarker

from datasets.datasets import getDataset
from plotter import SingleCellPlotter,CombinedImshowPlotter,RecurrenceStatScatter
from transformations.transformations import TransformationPipeline, ManualBoundaryClipping, NormalizedByMax, SavGolFilter, Difference, Thresholding
from transformations.tisean_wrapper import TiseanTransformation
from filters import MinConsecutiveLengthFilter,ManualFilter
import numpy
import matplotlib.pylab as plt
from scipy.stats import anderson

dataset = getDataset("hke3_batch1")

tp = TransformationPipeline([ManualBoundaryClipping(),BaselineCorrection(5),Thresholding(threshold=0.05)])
f = ManualFilter()

plotter = CombinedImshowPlotter(dataset,tp,f)
plotter.plot()
