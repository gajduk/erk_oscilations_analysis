import numpy as np

good_cells_longtime = {(1, 1), (1, 2), (10, 1), (4, 1), (4, 2), (4, 4), (4, 5), (6, 1), (6, 2), (6, 5), (7, 1), (7, 2),
                       (7, 3), (7, 4), (7, 5), (8, 1), (8, 2), (9, 3), (12, 1), (12, 2), (13, 1), (13, 4), (15, 1),
                       (15, 2), (15, 3), (15, 4), (16, 1), (16, 2), (16, 3), (16, 4), (16, 5), (17, 1), (17, 2),
                       (17, 3), (17, 4), (18, 1), (19, 1), (19, 2), (19, 3), (20, 1), (20, 2), (31, 1), (31, 2),
                       (33, 1), (33, 2), (33, 3), (34, 1), (34, 2), (40, 2), (21, 1), (21, 2), (23, 1), (23, 2),
                       (23, 3), (23, 4), (23, 5), (24, 1), (24, 2), (24, 3), (25, 2), (25, 3), (25, 4), (30, 1),
                       (30, 2)}


class NoFilter:
	def __init__(self):
		pass

	def filter(self, ts, position, cell_idx):
		return False

	def __str__(self):
		return "NoFilter"


class Close_to_1_Fitler:
	def __init__(self):
		pass

	def filter(self, ts, position, cell_idx):
		count = 0
		for e in ts:
			if 1.0 - e > .1:
				count += 1
		return count <= 2

	def __str__(self):
		return "CloseTo1"


class GoodCellFilter:
	def __init__(self, good_cells=good_cells_longtime):
		self._good_cells = good_cells

	def filter(self, ts, position, cell_idx):
		if (position, cell_idx) in self._good_cells:
			return False
		return True

	def __str__(self):
		return "GoodCells"


class NanAndCloseTo1Filter:
	def __init__(self, good_percent=0.6):
		self._good_percent = good_percent

	def filter(self, ts, position, cell_idx):
		count_nan, count_1, count_good = 0, 0, 0
		for e in ts:
			if np.isnan(e):
				count_nan += 1
			elif 1.0 - e < .05:
				count_1 += 1
			else:
				count_good += 1
		return count_good * 1.0 / len(ts) < self._good_percent

	def __str__(self):
		return "NanAndCloseTo1 " + str(self._good_percent)


class MinConsecutiveLengthFilter:
	def __init__(self, l=50):
		self.l = l

	def filter(self, ts, position, cell_idx):
		i = 0
		ll = 0
		if position == "060":
			return True
		while i < len(ts):
			while i < len(ts) and not np.isnan(ts[i]):
				ll += 1
				i += 1
			if ll > self.l:
				return False
			i += 1
			ll = 0
		return True

	def __str__(self):
		return "MinLength " + str(self.l)
