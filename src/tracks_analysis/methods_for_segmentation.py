import cv2
import matplotlib.gridspec as gridspec
import matplotlib.pylab as plt
import numpy as np
from PIL import Image
from pylab import get_cmap
from scipy.stats.kde import gaussian_kde

from tif import loadtiffstack
from tracks_module import loadAll
from utils import STACKS


def maskimage2cv(im):
	"""
	convert a mask image (with multiple masks) into cv2 contours

	Paramters
	----------

	im: mask image

	Returns
	--------

	contours: cv2 contours (list of np arrays)

	"""
	contours = []
	for n in np.unique(im)[1:]:
		im_obj = im == n
		contour = cv2.findContours(im_obj.astype("uint8"), cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
		# ix = np.argmax([len(x) for x in contour])
		contour = [(ee[0][0], ee[0][1]) for e in contour[1] for ee in e]
		contours.append(contour)

	return contours


def basicCircle(x, y, r, im):
	h, w = im.shape
	xi, yi, ri = int(x), int(y), int(r)
	coords = []
	cx = xi
	cy = yi
	for y in range(yi - 4 - ri, yi + 4 + ri):
		if 0 <= y < h:
			for x in range(xi - ri - 4, xi + ri + 4):
				if 0 <= x < w:
					dx = x - cx
					dy = y - cy
					if dx * dx + dy * dy <= ri * ri + 1:
						coords.append((y, x))
	return coords


def extendedCircle(x, y, r, im):
	h, w = im.shape
	xi, yi, ri = int(x), int(y), int(r)
	coords = []
	cx = xi
	cy = yi
	for y in range(yi - 8 * ri, yi + 8 + ri):
		if 0 <= y < h:
			for x in range(xi - 8 - ri, xi + ri + 8):
				if 0 <= x < w:
					dx = x - cx
					dy = y - cy
					if dx * dx + dy * dy <= 1.251 * (1.5 + ri) * (1.5 + ri):
						coords.append((y, x))
	return coords


methods = {'basicCircle': basicCircle, 'extendedCircle': extendedCircle}


def plotContourAndHist(x, y, r, im, method, color, sb):
	h, w = im.shape
	xi, yi = int(x), int(y)
	coords = methods[method](x, y, r, im)
	mask = np.zeros((h, w))
	temp = []
	for y, x in coords:
		temp.append(im[y][x])
		mask[y][x] = 1
	contours = maskimage2cv(mask)
	plt.subplot(sb[1])
	plt.fill([e[0] - (xi - 50) for e in contours[0]], [e[1] - (yi - 50) for e in contours[0]], color=color,
	         linewidth=3, fill=False)
	temp = [e for e in temp if not np.isnan(e)]
	temp.sort()
	n = len(temp)
	ends = int(n / 20)
	temp = temp[ends:-ends]
	kde = gaussian_kde(temp)
	# these are the values over wich your kernel will be evaluated
	dist_space = np.linspace(min(temp), max(temp), 100)
	# plot the results
	plt.subplot(sb[0])
	plt.plot(dist_space, kde(dist_space), color=color, linewidth=1)
	plt.axvline(x=np.nanmedian(temp), ymin=0, ymax=1, color=color)
	plt.tick_params(axis='both', left='off', top='off', right='off', bottom='on', labelleft='off', labeltop='off',
	                labelright='off', labelbottom='on')


def plotSingleFrame(im, im_cfpyfp, td, ti, tdi, s_pos, methods_and_colors):
	plt.figure(figsize=(10, 8))
	gs = gridspec.GridSpec(2, 2, width_ratios=[1, 1], height_ratios=[1, 4])
	x, y, r = td.poss[ti]
	plt.subplot(gs[2])
	plt.imshow(im[y - 50:y + 50, x - 50:x + 50], interpolation='none', aspect='auto', vmin=0.65, vmax=1.25,
	           cmap=get_cmap('hot'))
	plt.xlim([0, 100])
	plt.ylim([0, 100])
	plt.axis('off')

	for method, color in methods_and_colors:
		plotContourAndHist(x, y, r, im, method, color, sb=(gs[0], gs[2]))

	plt.subplot(gs[3])

	plt.imshow(im_cfpyfp[y - 50:y + 50, x - 50:x + 50], interpolation='none', aspect='auto', cmap=get_cmap('hot'))
	plt.xlim([0, 100])
	plt.ylim([0, 100])
	plt.axis('off')
	plt.text(83, 85, 'i:' + str(tdi), color='green')
	plt.text(83, 90, 't:' + str(ti + 1), color='green')
	plt.text(83, 95, 'p:' + s_pos, color='green')

	for method, color in methods_and_colors:
		plotContourAndHist(x, y, r, im_cfpyfp, method, color, sb=(gs[1], gs[3]))
		plt.tight_layout()
	plt.savefig(s_pos + "_" + str(tdi) + "_" + str(ti + 1) + ".png")
	plt.close()


def getSnapshotIndexes(tps):
	res = {}
	n_snapshots = 9
	for tdi, td in enumerate(tps.tracks):
		tis = [ti for ti in range(300) if not td.poss[ti] == -1]
		tis.sort()
		step = len(tis) / (n_snapshots - 1)
		t_indexes = []
		for i in range(n_snapshots - 1):
			t_indexes.append(int(i * step))
		t_indexes.append(tis[-5])
		res[tdi] = t_indexes
	return res


def testMethod(methods_and_colors):
	trackss = loadAll(True)
	for s_pos in sorted(trackss):
		tps = trackss[s_pos]

		print "###############"
		print s_pos
		try:
			ratio_stack = loadtiffstack(STACKS + "Ratio " + s_pos + ".tif")
			im = ratio_stack.next()
			cfpyfp_stack = loadtiffstack(STACKS + s_pos + " CFP YFP.TIF")
			im_cfpyfp = cfpyfp_stack.next()
		except:
			return -1
		track_snapshots_ti = getSnapshotIndexes(tps)

		for ti in range(300):
			h, w = im.shape
			for tdi, td in enumerate(tps.tracks):
				if ti in track_snapshots_ti[tdi]:
					plotSingleFrame(im, im_cfpyfp, td, ti, tdi, s_pos, methods_and_colors)
			if ti < 299:
				im = ratio_stack.next()
				im_cfpyfp = cfpyfp_stack.next()

		for tdi, td in enumerate(tps.tracks):
			# combine all the pngs
			list_im = []
			for ti in track_snapshots_ti[tdi]:
				img_filename = s_pos + "_" + str(tdi) + "_" + str(ti + 1) + ".png"
				list_im.append(img_filename)
			imgs = [Image.open(i) for i in list_im]
			imgs_comb1 = np.hstack((imgs[i] for i in [0, 1, 2]))
			imgs_comb2 = np.hstack((imgs[i] for i in [3, 4, 5]))
			imgs_comb3 = np.hstack((imgs[i] for i in [6, 7, 8]))
			imgs_comb = np.vstack((imgs_comb1, imgs_comb2, imgs_comb3))
			imgs_comb = Image.fromarray(imgs_comb)
			imgs_comb.save(s_pos + "_" + str(tdi) + ".png")
		break


if __name__ == '__main__':
	testMethod([('basicCircle', 'black'), ('extendedCircle', 'blue')])
