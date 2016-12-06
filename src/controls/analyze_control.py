import os
import matplotlib.pylab as plt
import numpy as np
import matplotlib.patches as mpatches

foldername = """C:\Users\gajduk\Google Drive\DATA\MDCK EKAREV\hke3 11_11_16\processed"""

#file format:  cell_line (1 space) pre or post (space) position.txt

def errorfill(x, y, yerr, color=None, alpha_fill=0.3, ax=None):
    ax = ax if ax is not None else plt.gca()
    if color is None:
        color = ax._get_lines.color_cycle.next()
    if np.isscalar(yerr) or len(yerr) == len(y):
        ymin = y - yerr
        ymax = y + yerr
    elif len(yerr) == 2:
        ymin, ymax = yerr
    ax.plot(x, y, color=color)
    ax.fill_between(x, ymax, ymin, color=color, alpha=alpha_fill)

class SingleCell:
	pre_values = -1
	post_vaues = -1
	position = -1
	roi = -1
	cell_line = -1

	def __init__(self,cell_line,position,roi_idx):
		self.position = position
		self.roi_idx = roi_idx
		self.cell_line = cell_line

	def plot(self):
		y1 = [e for e in self.pre_values]
		y2 = [e for e in self.post_values]
		x1 = [i for i,e in enumerate(self.pre_values)]
		x2 = [i+26 for i,e in enumerate(self.pre_values)]
		ax = plt.plot(x1,y1,'b')
		ax = plt.plot(x2,y2,'b')
		plt.xlabel('Time [min]')
		plt.ylabel('CFP_YFP/CFP')
		plt.title(self.cell_line+"  "+str(self.position)+"-"+str(self.roi_idx))
		plt.axvline(x=25, ymin=0, ymax = 2, linewidth=1, color='r')
		plt.text(25.5,min(min(y2),min(y1)),"egf", color='r')

class Dataset:

	mapa = -1#keys are (position,roi_idx), values are SingleCell

	def __init__(self,cell_line):
		self.cell_line = cell_line
		self.mapa = {}

	def plotAverageNormalized(self,color='b',normalization='none'):
		yy1,yy2 = [],[]
		xx1,xx2 = [],[]
		for tuple_ in self.mapa:
			single_cell = self.mapa[tuple_]
			norm_val = np.mean([e for e in single_cell.pre_values])
			if normalization == 'none':
				yy1.append([e for e in single_cell.pre_values])
				yy2.append([e for e in single_cell.post_values])
			if normalization == 'divide':
				yy1.append([e/norm_val for e in single_cell.pre_values])
				yy2.append([e/norm_val for e in single_cell.post_values])
			if normalization == 'subtract':
				yy1.append([e-norm_val for e in single_cell.pre_values])
				yy2.append([e-norm_val for e in single_cell.post_values])

			xx1 = [i for i,e in enumerate(single_cell.pre_values)]
			xx2 = [i+26 for i,e in enumerate(single_cell.pre_values)]
		mult = np.sqrt(len(yy1)/5)/2
		errorfill(xx1,np.mean(yy1,axis=0),np.var(yy1,axis=0)*mult,color)
		errorfill(xx2,np.mean(yy2,axis=0),np.var(yy2,axis=0)*mult,color)
		plt.xlabel('Time [min]')
		plt.ylabel('FRET/CFP')
		plt.axvline(x=25, ymin=0, ymax = 2, linewidth=1, color='r')
	
	def plotSeparate(self):
		plt.figure(figsize=(15,17))
		i = 1
		for tuple_ in self.mapa:
			plt.subplot(6,5,i)
			i += 1
			self.mapa[tuple_].plot()
		plt.tight_layout()


def parseResults(cell_line="hke3"):
	mapp = {"100ng OLD":"hke3","100ng":"hke3control100ng","200pg":"hke3control200pg","600pg":"hke3control200pg"}
	bad_tuples = {"100ng OLD":[(2,2),(3,2),(2,3),(10,2),(4,2)],
		"100ng":[(2,2),(2,3)],"200pg":[(3,2),(3,1),(4,2)],
		"600pg":[(7,0),(10,2)]}
	cell_line_s = mapp[cell_line]
	res = Dataset(cell_line)
	onlyfiles = [f for f in os.listdir(foldername) if f.endswith(".txt") and f.startswith(cell_line_s) ]
	for file in onlyfiles:
		s_file = file[:-4].split(" ")
		#cell_line = s_file[0]
		pre_or_post = s_file[-2]
		s_position = s_file[-1]
		if len(s_file) == 4:
			s_position = s_file[1]+s_position
		position = int(s_position)
		if cell_line == "200pg":
			if position > 5:
				continue
		if cell_line == "600pg":
			if position <= 5:
				continue
		with open(foldername+"\\"+file,"r") as pin:
			rois = pin.read().split("ROI:")[1:]
			for roi in rois:
				lines = roi.split('\n')
				roi_idx = int(lines[0])
				values = []
				for line in lines[1:]:
					if "\t" in line:
						values.append(float(line.split("\t")[1]))
				tuple_ = (position,roi_idx)
				if tuple_ in bad_tuples[cell_line]:
					continue
				sc = SingleCell(cell_line,position,roi_idx)
				if tuple_ in res.mapa:
					sc = res.mapa[tuple_]
				if "pre" in pre_or_post:
					sc.pre_values = values
				else:
					sc.post_values = values
				res.mapa[tuple_] = sc
	return res

def plotCombined(normalization):
	datasets = []

	cell_lines = ["100ng OLD","100ng","200pg","600pg"]
	colors = ["m","b","g","r"]

	for i,cell_line in enumerate(cell_lines):
		datasets.append(parseResults(cell_line=cell_line))
		datasets[i].plotAverageNormalized(color=colors[i],normalization=normalization)

	plt.legend(loc='upper left',handles=[ mpatches.Patch(color=colors[i], label=cell_lines[i]) for i in range(4)])

	plt.text(25.5,0.955,"egf", color='r')
	plt.title('normalized to pre stimulation\n'+normalization)
	plt.tight_layout()
	plt.savefig(normalization+" combined_control.png",dpi=600)
	plt.close()

def plotSeparate():
	cell_lines = ["100ng OLD","100ng","200pg","600pg"]
	for i,cell_line in enumerate(cell_lines):
		parseResults(cell_line=cell_line).plotSeparate()
		plt.savefig(cell_line+"_control.png",dpi=600)
		plt.close()

plotCombined('none')
plotCombined('divide')
plotCombined('subtract')