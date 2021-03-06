
from tracks_analysis.tif import loadtiffstack

import matplotlib.pylab as plt
import numpy as np
import matplotlib

file = "E:\\Ratio of 4x10e4 002 CFP_YFP.tif"

medians  = [0.89009333, 0.88156796, 0.87812841, 0.8763206, 0.87524754, 0.87616885, 0.87177539, 0.87455833, 0.8720845, 0.87987518, 0.89516127, 0.90957165, 0.91217458, 0.90801299, 0.90165019, 0.89581245, 0.89014953, 0.88843465, 0.88816035, 0.88776541, 0.89023715, 0.89108348, 0.89604688, 0.89939332, 0.90387374, 0.91455275, 0.91819614, 0.91183114, 0.91228068, 0.91270459, 0.90930289, 0.90605098, 0.9004271, 0.89802629, 0.89618063, 0.89413989, 0.89075089, 0.89534885, 0.89592367, 0.89698493, 0.90904784, 0.92163545, 0.92699015, 0.92553192, 0.92503089, 0.91973734, 0.91815323, 0.91600108, 0.91025639, 0.9087221, 0.90415335, 0.90255904, 0.90163022, 0.89980674, 0.90021771, 0.90360165, 0.91015172, 0.91989666, 0.93035114, 0.93552464, 0.93730438, 0.93504274, 0.92847502, 0.92263877, 0.91690981, 0.91360688, 0.91299433, 0.90939373, 0.90743154, 0.90636706, 0.90598983, 0.90510947, 0.90675962, 0.90643275, 0.90794575, 0.90742797, 0.90685773, 0.90631932, 0.90777576, 0.90890586, 0.91151386, 0.91168344, 0.91027498, 0.91601866, 0.91662037, 0.92134833, 0.93220341, 0.94622791, 0.9531129, 0.95197707, 0.94511962, 0.93898302, 0.93250442, 0.92647636, 0.92356789, 0.92277229, 0.92021275, 0.920084, 0.92036122, 0.92205685]

xs = [4,19,33,53,77,97]
ys = [0.875,0.889,0.894,0.9,0.907,0.92]

x = [e for e in range(100)]
z = np.polyfit(xs, ys, 4)
p = np.poly1d(z)


def get_time_s(i):
	hour = str(int(i/12))
	min = str((i%12)*5)
	if len(min) == 1:
		min = "0"+min
	return hour+":"+min


ratio_stack = loadtiffstack(file)
#plt.figure(figsize=(30,20))
for i in range(100):
	plt.figure(figsize=(3, 3))
	im = ratio_stack.next()
	cell_im = im[170:265,430:560]-p(i)
	#plt.subplot(8,12,i-3)
	masked_array = np.ma.array(cell_im, mask=np.isnan(cell_im))
	cmap = matplotlib.cm.jet
	cmap.set_bad('black', 1.)
	plt.imshow(cell_im,interpolation='none',cmap=cmap,vmin=-0.05,vmax=+0.05)
	plt.axis('off')
	plt.tight_layout()
	plt.text(x=105,y=90,s=get_time_s(i), color='green')
	plt.savefig("E:\\asd\\"+str(i)+' showcase.png',dpi=150)
	plt.close()
	print i
#plt.tight_layout()
#plt.show()


