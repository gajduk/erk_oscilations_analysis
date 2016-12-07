import pickle

import matplotlib.pylab as plt
import numpy as np

from tif import loadtiffstack
from tracks_module import loadAll
from methods_for_segmentation import methods
from utils import STACKS,DATA,FIGURES


def getValues(tps,method='extendedCircle'):
	s_pos = tps.s_pos
	if method not in methods:
		print "ERROR method:"+method+" not in methods:"+str(methods)
		return None
	print "###############"
	print s_pos
	try:
		stack = loadtiffstack("Ratio " + s_pos + ".tif")
		im = stack.next()
	except:
		return -1
	values = [[float('NaN') for e in range(300)] for e in tps.tracks]
	for ti in range(300):
		h, w = im.shape
		if ti % 30 == 0:
			print ti
		for tdi, td in enumerate(tps.tracks):
			if not td.poss[ti] == -1:
				x, y, r = td.poss[ti]
				coords = methods[method](x,y,r,im)
				temp = []
				for y,x in coords:
					temp.append(im[y][x])
				values[tdi][ti] = np.nanmedian(temp)
		if ti < 299:
			im = stack.next()
	return values



def computeAllValues(cache):
	if cache:
		return pickle.load(open(DATA+"values", "r"))
	trackss = loadAll(True)
	valuess = {}
	for s_pos in sorted(trackss):
		tps = trackss[s_pos]
		values = getValues(tps)
		if not values == -1:
			valuess[s_pos] = values
	pickle.dump(valuess, open(DATA+"values", "w"))
	return valuess


def getegf(s_pos):
	pos = int(s_pos)
	if pos < 15:
		return "  0 pg"
	elif pos < 26:
		return " 10 pg"
	elif pos < 47:
		return "100 pg"
	else:
		return "600 pg"


def plotAllOnOnePLot():
	trackss = loadAll(True)
	valuess = computeAllValues(True)
	plt.figure(figsize=(42, 30))
	i = 0
	for s_pos in sorted(valuess):
		tracks = trackss[s_pos].tracks
		for idx, value in enumerate(valuess[s_pos]):
			if np.count_nonzero(~np.isnan(value)) < 80:
				continue
			if idx == 0 and s_pos == "052":
				continue
			track = tracks[idx]
			i += 1
			plt.subplot(7, 8, i)
			plt.plot(value)
			for t in track.special_events:
				s = track.special_events[t]
				marker = 'o'  # dissapear
				color = 'gray'
				if 'DEATH' in s:
					marker = 'd'
					color = 'red'
				if 'DIVIS' in s:
					if 'START' in s:
						marker = 'v'
						color = 'yellow'
					else:
						marker = '^'
						color = 'green'
				plt.plot(t, value[t], marker=marker, markersize=10, color=color)
			plt.title(getegf(s_pos) + " egf (" + s_pos + ":" + str(idx) + ")")

			plt.xlabel('Time [1 frame = 10 mins]')
			plt.ylabel('FRET/CFP')
			plt.xlim([0, 300])
			plt.ylim([0.6, 1.2])
	plt.tight_layout()
	plt.savefig(FIGURES+'raw_data_plot.png', dpi=300)


def plotAllOnSeparatePlots():
	trackss = loadAll(True)
	valuess = computeAllValues(True)
	for egf in ["  0 pg", " 10 pg", "100 pg", "600 pg"]:
		plt.figure(figsize=(25, 25))
		i = 0
		for s_pos in sorted(valuess):
			if not getegf(s_pos) == egf:
				continue
			tracks = trackss[s_pos].tracks
			for idx, value in enumerate(valuess[s_pos]):
				if np.count_nonzero(~np.isnan(value)) < 80:
					continue
				if idx == 0 and s_pos == "052":
					continue
				track = tracks[idx]
				i += 1
				plt.subplot(9, 9, i)
				plt.plot(value)
				for t in track.special_events:
					s = track.special_events[t]
					marker = 'o'  # dissapear
					color = 'gray'
					if 'DEATH' in s:
						marker = 'd'
						color = 'red'
					if 'DIVIS' in s:
						if 'START' in s:
							marker = 'v'
							color = 'yellow'
						else:
							marker = '^'
							color = 'green'
					plt.plot(t, value[t], marker=marker, markersize=10, color=color)
				plt.title(getegf(s_pos) + " egf (" + s_pos + ":" + str(idx) + ")")

				plt.xlabel('Time [1 frame = 10 mins]')
				plt.ylabel('FRET/CFP')
				plt.xlim([0, 300])
				plt.ylim([0.6, 1.2])
		plt.tight_layout()
		plt.savefig(FIGURES+'raw_data_' + egf + '.png', dpi=300)


def main():
	plotAllOnSeparatePlots()


if __name__ == "__main__":
	main()
