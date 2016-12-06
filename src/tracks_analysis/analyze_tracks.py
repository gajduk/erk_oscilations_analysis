import pickle

import matplotlib.pylab as plt
import numpy as np

from tif import loadtiffstack
from tracks_module import loadAll


def makeCircle():
	cache = {}

	def get(ri):
		if ri not in cache:
			mask = np.zeros((ri * 2, ri * 2))

			for x in range(ri * 2):
				for y in range(ri * 2):
					dx = x - (ri - 0.5)
					dy = y - (ri - 0.5)
					if dx * dx + dy * dy <= ri * ri:
						mask[x, y] = 1
			cache[ri] = mask
		return cache[ri]

	return get


circles = makeCircle()


def getValues(tps):
	s_pos = tps.s_pos
	print "###############"
	print s_pos
	try:
		stack = loadtiffstack("E:\\hke3 11_11_16\\hke3 longtime\\Ratio " + s_pos + ".tif")
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
				xi, yi, ri = int(x), int(y), int(r)
				temp = []
				# pixels,p1 = [],[]
				cx = x + ri
				cy = y - ri
				for y in range(yi - 4 - 2 * ri, yi + 4):
					if y >= 0 and y < h:
						for x in range(xi - 4, xi + 2 * ri + 4):
							if x >= 0 and x < w:
								dx = x - cx
								dy = y - cy
								if dx * dx + dy * dy <= 1.251 * (1.5 + ri) * (1.5 + ri):
									temp.append(im[y][x])
									''' debugging to see circle
									pixels.append((y,x))
								if dx*dx+dy*dy <= ri*ri:
									p1.append((y,x))

				for y,x in pixels:
					im[y][x] = 5
				for y,x in p1:
					im[y][x] = 10
				plt.imshow(im,interpolation='none')
				plt.show()
				quit()
				'''
				values[tdi][ti] = np.nanmedian(temp)

		if ti < 299:
			im = stack.next()
	return values


def computeAllValues(cache):
	if cache:
		return pickle.load(open("..\\data\\values", "r"))
	trackss = loadAll(cache)
	valuess = {}
	for s_pos in sorted(trackss):
		tps = trackss[s_pos]
		values = getValues(tps)
		if not values == -1:
			valuess[s_pos] = values
	pickle.dump(valuess, open("..\\data\\values", "w"))
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
	trackss = loadAll()
	valuess = computeAllValues()
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
	plt.savefig('raw_data_plot.png', dpi=300)


def plotAllOnSeparatePlots():
	trackss = loadAll()
	valuess = computeAllValues()
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
		plt.savefig('raw_data_' + egf + '.png', dpi=300)


def main():
	plotAllOnSeparatePlots()


if __name__ == "__main__":
	main()
