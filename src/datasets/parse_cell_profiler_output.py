from core import SingelCellSingleFrameData,SingleCellMovieData,SingleConditionData,Dataset
from tracks_analysis.analyze_tracks import computeAllValues


class DatasetBuilder:

	def __init__(self,condition_ranges,nframes,frame_length_in_minutes):
		self.scsfd = []
		self.condition_ranges = condition_ranges
		self.nframes = nframes
		self.frame_length_in_minutes = frame_length_in_minutes

	def add_scsfd(self,scsfd):
		self.scsfd.append(scsfd)

	def build(self):
		scmd = {}
		for scsfd in self.scsfd:
			tuple_ = (scsfd._position,scsfd._cell_idx)
			if tuple_ not in scmd:
				scmd[tuple_] = []
			o = scmd[tuple_]
			o.append(scsfd)
			scmd[tuple_] = o
		temp = []
		for tuple_ in scmd:
			scmd[tuple_].sort(key=lambda x: x._frame_idx)
			asd = {e._frame_idx:e for e in scmd[tuple_]}
			for i in range(1,self.nframes+1):
				if i not in asd:
					asd[i] = SingelCellSingleFrameData(tuple_[0],i,tuple_[1],float('nan'))
			temp.append(SingleCellMovieData([asd[i] for i in range(1,self.nframes+1)],self.nframes))
		scmd = temp

		scd = {}

		for qwe in scmd:
			condition_label = self._findConditionLabel(qwe._position)
			if condition_label not in scd:
				scd[condition_label] = []
			o = scd[condition_label]
			o.append(qwe)
			scd[condition_label] = o

		temp = []

		for qwe in scd:
			temp.append(SingleConditionData(scd[qwe],qwe,self.nframes))
		temp = [temp[i] for i in [1,3,0,2]]
		return Dataset(temp,self.nframes,self.frame_length_in_minutes)


	def _findConditionLabel(self,position):
		max_ = 1
		for key in self.condition_ranges:
			if key < position and key > max_:
				max_ = key
		return self.condition_ranges[max_]

class DataReaderAndParser:

	def __init__(self,condition_ranges,nframes,file,frame_length_in_minutes=10):
		self._file = file
		self._condition_ranges = condition_ranges
		self._nframes = nframes
		self._frame_length_in_minutes = frame_length_in_minutes

	def read(self):			
		builder = DatasetBuilder(self._condition_ranges,self._nframes,self._frame_length_in_minutes)
		with open(self._file,"r") as pin:
			pin.readline()
			line_number = 1
			for line in pin:
				try:
					s_line = line.split(",")
					cell_idx = int(s_line[1])
					frame_idx = int(s_line[4])
					position = int(s_line[6])
					mean_int = float(s_line[16])
					builder.add_scsfd(SingelCellSingleFrameData(position,frame_idx,cell_idx,mean_int))
				except:
					pass
				line_number += 1
		return builder.build()


class HkeReaderBatch1:

	def __init__(self):
		pass

	def read(self):
		valuess = computeAllValues(True)

		scmds = {}
		for s_pos in valuess:
			pos = int(s_pos)
			if pos < 15:
				egf = "  0 pg"
			elif pos < 26:
				egf = " 10 pg"
			elif pos < 47:
				egf = "100 pg"
			else:
				egf = "600 pg"
			cells = valuess[s_pos]
			for i in range(len(cells)):
				position = s_pos
				cell_idx = i
				nframes = 300
				scsfd = []
				for k in range(300):
					scsfd.append(SingelCellSingleFrameData(position,k,cell_idx,cells[i][k]))
				scmd = SingleCellMovieData(scsfd,nframes)
				o = []
				if egf in scmds:
					o = scmds[egf]
				o.append(scmd)
				scmds[egf] = o
		scds = []
		for egf in ["  0 pg"," 10 pg","100 pg","600 pg"]:
			scds.append(SingleConditionData(scmds[egf],egf,300))
		return Dataset(scds,300,10)


if __name__ == "__main__":
	dataset = HkeReaderBatch1().read()