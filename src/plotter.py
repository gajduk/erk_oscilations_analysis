from os import makedirs
from os.path import exists
from time import gmtime, strftime

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from filters import recurenceplot
from recurence_plot_quantifications import get_rp, lam, rr
from transformations.peakutils_wrapper import PeakDetection
from transformations.transformations import removeNans

default_figure_folder = "C:\\Users\\gajduk\\Desktop\\figs\\"


def find_median(combined):
	n = len(combined[0])
	x, median, st_quartile, rd_quartile = [], [], [], []
	for i in range(n):
		a = [c[i] for c in combined if not np.isnan(c[i])]
		median.append(np.percentile(a, 50))
		st_quartile.append(np.percentile(a, 25))
		rd_quartile.append(np.percentile(a, 75))
		x.append(i)
	return x, median, st_quartile, rd_quartile


def errorfill_from_matrix(combined, color=None, alpha_fill=0.3, ax=None):
	ax = ax if ax is not None else plt.gca()
	x, y, ymin, ymax = find_median(combined)

	if color is None:
		base_line, = ax.plot(x, y)
	else:
		base_line, = ax.plot(x, y, color=color)

	ax.fill_between(x, ymax, ymin, color=base_line.get_color(), alpha=alpha_fill)


class Plotter:
	def __init__(self, dataset, transformation, filter_):
		self._dataset = dataset
		self._transformation = transformation
		self._filter = filter_
		self._folder = default_figure_folder + strftime("%H_%M_%S %d_%m_%Y", gmtime()) + "  " + self.get_label() + "\\"
		if not exists(self._folder):
			makedirs(self._folder)

	def plot(self):
		pass

	def is_cell_filtered(self, scmd):
		position = scmd._position
		cell_idx = scmd._cell_idx
		ts = scmd.get_time_series()
		return self._filter.filter(ts, position, cell_idx)

	def get_time_series(self, scmd):
		position = scmd._position
		cell_idx = scmd._cell_idx
		return self._transformation.transform(scmd.get_time_series(), (position, cell_idx))

	def get_label(self):
		return "F_" + str(self._filter) + " T_" + str(self._transformation)


class ShowcaseCellPlotter(Plotter):

	def __init__(self, dataset, transformation, filter_):
		Plotter.__init__(self, dataset, transformation, filter_)

	def plot(self):
		for scd in self._dataset._scd:  # iterate over conditions
			xticks = [i * 6 * 2 for i in range(17)]
			xlabels = ['' if i % 4 > 0 else str(i * 2) for i in range(17)]
			for scmd in scd._scmd:  # iterate over cells
				if self.is_cell_filtered(scmd):
					continue
				print scmd
				ts = self.get_time_series(scmd)
				from recurence_plot_quantifications import get_rp
				rp = get_rp(ts,de = 0.00002)
				plt.figure(figsize=(3, 3))
				plt.imshow(1-rp,cmap='gray',interpolation='none')
				plt.xlim([0, 200])
				plt.ylim([0, 200])
				plt.xticks(xticks,xlabels)
				plt.yticks(xticks,xlabels)
				plt.xlabel('Time [Hours]',fontweight='bold')
				plt.ylabel('Time [Hours]',fontweight='bold')
				plt.tight_layout()
				plt.savefig(self.get_filename(scd, scmd), transparent=True, dpi=1200)
				plt.close()

	def get_filename(self, scd, scmd):
		return self._folder + self.get_title(scd, scmd) + ".png"

	def get_title(self, scd, scmd):
		return str(scd._condition_label) + " " + str(scmd._position) + " " + str(scmd._cell_idx)

	def plot_internal(self, ts):
		plt.plot(ts)

class SingleCellPlotter(Plotter):
	def __init__(self, dataset, transformation, filter_, ylim=[-0.1, 0.2]):
		Plotter.__init__(self, dataset, transformation, filter_)
		self.ylim = ylim

	def plot(self):
		for scd in self._dataset._scd:  # iterate over conditions
			xticks = [i*6*2 for i in range(17)]
			xlabels = ['' if i%4>0 else str(i*2) for i in range(17)]
			for scmd in scd._scmd:  # iterate over cells
				if self.is_cell_filtered(scmd):
					continue
				print scmd
				ts = self.get_time_series(scmd)
				plt.figure(figsize=(6, 3))
				self.plot_internal(ts)
				plt.xlabel('Time [Hours]',fontweight='bold')
				#plt.title(self.get_title(scd, scmd))
				plt.xticks(xticks,xlabels)
				# plt.yticks(yticks,ylabels)
				plt.ylabel('pERK\n(FRET/CFP)',fontweight='bold')
				plt.xlim([0, 200])
				plt.ylim(self.ylim)
				plt.tight_layout()
				plt.grid()
				#plt.show()
				plt.savefig(self.get_filename(scd, scmd), transparent=True, dpi=300)
				plt.close()

	def get_filename(self, scd, scmd):
		return self._folder + self.get_title(scd, scmd) + ".png"

	def get_title(self, scd, scmd):
		return str(scd._condition_label) + " " + str(scmd._position) + " " + str(scmd._cell_idx)

	def plot_internal(self, ts):
		plt.plot(ts)


class SingleCellRecurrencePlotter(Plotter):
	def __init__(self, dataset, transformation, filter_, ylim=[-0.1, 0.2]):
		Plotter.__init__(self, dataset, transformation, filter_)
		self.ylim = ylim

	def plot(self):
		for scd in self._dataset._scd:  # iterate over conditions
			# xticks = [i*6*4 for i in range(11)]
			# xlabels = [''if i%2==1 else str(i*4)  for i in range(11)]
			for scmd in scd._scmd:  # iterate over cells
				if self.is_cell_filtered(scmd):
					continue
				print scmd
				ts = self.get_time_series(scmd)
				plt.figure(figsize=(8, 12))
				plt.subplot(2, 1, 1)
				self.plot_internal(ts)
				plt.xlabel('Frame [' + str(self._dataset._frame_length_in_minutes) + ' min]')
				plt.title(self.get_title(scd, scmd))
				# plt.xticks(xticks,xlabels)
				# plt.yticks(yticks,ylabels)
				plt.xlim([0, self._dataset._nframes])
				plt.ylim(self.ylim)
				plt.tight_layout()
				plt.grid()

				plt.subplot(2, 1, 2)

				recurenceplot(np.array(removeNans(ts))[0], de=.04)
				plt.savefig(self.get_filename(scd, scmd), transparent=True, dpi=500)
				plt.close()

	def get_filename(self, scd, scmd):
		return self._folder + self.get_title(scd, scmd) + ".png"

	def get_title(self, scd, scmd):
		return str(scd._condition_label) + " " + str(scmd._position) + " " + str(scmd._cell_idx)

	def plot_internal(self, ts):
		plt.plot(ts)


class SingleCell3DPlotter(Plotter):
	def __init__(self, dataset, transformation, filter_):
		Plotter.__init__(self, dataset, transformation, filter_)

	def plot(self):
		for scd in self._dataset._scd:  # iterate over conditions
			for scmd in scd._scmd:  # iterate over cells
				if self.is_cell_filtered(scmd):
					continue
				ts = self.get_time_series(scmd)
				fig = plt.figure(figsize=(8, 6))
				mpl.rcParams['lines.linewidth'] = 2
				ax = fig.add_subplot(111, projection='3d')
				plt.title(self.get_title(scd, scmd))
				ax.set_xlabel('x(t-2)', linespacing=3.2)
				ax.set_ylabel('x(t-1)', linespacing=3.1)
				ax.set_zlabel('x(t)', linespacing=3.4)
				ax.dist = 10
				self.plot_internal(ax, ts)
				plt.grid()
				ax.w_xaxis._axinfo.update({'grid': {'color': (0, 0, 0, 1)}})
				ax.w_yaxis._axinfo.update({'grid': {'color': (0, 0, 0, 1)}})
				ax.w_zaxis._axinfo.update({'grid': {'color': (0, 0, 0, 1)}})
				ax.set_ylim([0, 0.25])
				ax.set_zlim([0, 0.25])
				ax.set_xlim([0, 0.25])
				ax.view_init(30, 255)
				plt.savefig(self.get_filename(scd, scmd), transparent=True, dpi=600)
				plt.close()

	def get_filename(self, scd, scmd):
		return self._folder + self.get_title(scd, scmd) + ".png"

	def get_title(self, scd, scmd):
		return str(scd._condition_label) + " " + str(scmd._position) + " " + str(scmd._cell_idx)

	def plot_internal(self, ax, ts):
		ax.plot(ts[:-2], ts[1:-1], ts[2:])


class CombinedImshowPlotter(Plotter):
	def __init__(self, dataset, transformation, filter_):
		Plotter.__init__(self, dataset, transformation, filter_)

	def plot(self):
		plt.figure(figsize=(6, 6))
		subplot_idx = 1
		combined = None
		ytick_labels = []
		for scd_idx, scd in enumerate(self._dataset._scd):  # iterate over conditions
			plt.subplot(2, 2, subplot_idx)
			subplot_idx += 1
			# xticks = [i*6*4 for i in range(13)]
			# xlabels = [''if i%2==1 else str(i*6*4)  for i in range(13)]

			count = 0
			for idx, scmd in enumerate(scd._scmd):  # iterate over cells
				if self.is_cell_filtered(scmd):
					continue
				count += 1

			condition_y = np.zeros((count, scd._nframes))
			condition_y[:] = np.NAN
			count = 0
			for idx, scmd in enumerate(scd._scmd):  # iterate over cells
				if self.is_cell_filtered(scmd):
					continue
				ts = self.get_time_series(scmd)
				condition_y[count, :len(ts)] = ts
				ytick_labels.append(str(scmd)[5:])
				count += 1

			#
			if combined is None:
				combined = condition_y
				for zxcasd in range(4):
					ytick_labels.append(' ')
			else:
				a = np.zeros((4, scd._nframes))
				a[:] = np.NAN
				combined = np.vstack((combined, a, condition_y))
				for zxcasd in range(4):
					ytick_labels.append(' ')
			self.plot_internal(condition_y)
			plt.xlabel('Frame [' + str(self._dataset._frame_length_in_minutes) + ' min]')
			plt.title(self.get_title(scd))
			# plt.xticks(xticks,xlabels)
			plt.xlim([0, self._dataset._nframes])
		plt.tight_layout()
		plt.savefig(self.get_filename(scd), dpi=300, transparent=True)
		plt.close()

		plt.figure(figsize=(6, 12))
		self.plot_internal(combined)

		plt.xlabel('Frame [' + str(self._dataset._frame_length_in_minutes) + ' min]')
		plt.title(self.get_title(scd))
		# plt.xticks(xticks,xlabels)
		plt.xlim([0, self._dataset._nframes])
		plt.yticks(range(len(ytick_labels)), ytick_labels, fontsize=5)
		plt.tight_layout()
		plt.text(300, 15, '  0 pg egf')
		plt.text(300, 35, ' 10 pg egf')
		plt.text(300, 60, '100 pg egf')
		plt.text(300, 100, '600 pg egf')
		plt.savefig(self._folder + "combined.png", dpi=300, transparent=True)
		plt.close()

	def get_filename(self, scd):
		return self._folder + self.get_title(scd) + ".png"

	def get_title(self, scd):
		return str(scd._condition_label)

	def plot_internal(self, ts):
		masked_array = np.ma.array(ts, mask=np.isnan(ts))
		cmap = plt.cm.jet
		cmap.set_bad('white', 1.1)
		plt.imshow(ts, aspect=10, interpolation='none', vmin=0, vmax=0.15)




class RecurrenceStatScatter(Plotter):
	def __init__(self, dataset, transformation, filter_):
		Plotter.__init__(self, dataset, transformation, filter_)

	def plot(self):
		xs_random, ys_random = [], []
		for k in np.linspace(0.15, 0.5, 200):
			n = 150
			x = np.zeros((n, n))
			x[np.random.rand(n, n) < k] = 1
			xs_random.append(rr(x))
			ys_random.append(lam(x, 3))

		xs, ys = [], []
		c = 0
		for scd_idx, scd in enumerate(self._dataset._scd):  # iterate over conditions
			for idx, scmd in enumerate(scd._scmd):  # iterate over cells
				if self.is_cell_filtered(scmd):
					continue
				ts = self.get_time_series(scmd)
				xs.append(rr(get_rp(ts, .008)))
				ys.append(lam(get_rp(ts, .008), 3))
				c += 1

		plt.figure(figsize=(5, 7))
		plt.scatter(xs, ys, marker='+', color='blue',label='Data')
		plt.scatter(xs_random, ys_random, marker='+', color='black',label='Random')
		plt.xlabel('Recurrence Rate')
		plt.ylabel('Trapping Time (Recurence plot statistics)')
		plt.legend()
		# plt.xlim([0-1,c+1])
		plt.ylim([1.8, 2.8])
		plt.tight_layout()
		plt.savefig(self._folder + "lam_rp.png", dpi=600, transparent=True)
		plt.close()


def plot_recurrence():
	from datasets.datasets import getDataset
	from transformations.transformations import TransformationPipeline
	from filters import GoodCellFilter, MinConsecutiveLengthFilter
	dataset = getDataset("hke3_batch1")
	a = {('0001', 0), ('003', 1), ('011', 0), ('011', 4), ('012', 4), ('013', 1), ('013', 2), ('063', 0)}
	filter = GoodCellFilter(a)
	filter = MinConsecutiveLengthFilter(120)
	plotter = SingleCellRecurrencePlotter(dataset, TransformationPipeline([]), filter, ylim=[0.6, 1.2])
	plotter.plot()


if __name__ == "__main__":
	plot_recurrence()
