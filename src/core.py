
class SingelCellSingleFrameData:

	_cell_idx = -1
	_frame_idx = -1
	_position = -1
	_mean_int = -1

	def __init__(self,position,frame_idx,cell_idx,mean_int):
		self._position = position
		self._frame_idx = frame_idx
		self._cell_idx = cell_idx
		self._mean_int = mean_int

	def __repr__(self):
		return "SCSFD "+str(self._position)+" "+str(self._cell_idx)+" "+str(self._frame_idx)+" "+str(self._mean_int)

class SingleCellMovieData:

	_scsfd = -1 #an array of SingelCellSingleFrameData
	_position = -1
	_cell_idx = -1
	_nframes = -1

	def __init__(self,scsfd,nframes):
		self._scsfd = scsfd
		self._nframes = nframes
		self._position = scsfd[0]._position
		self._cell_idx = scsfd[0]._cell_idx

	def get_time_series(self):
		return [e._mean_int for e in self._scsfd]

	def __repr__(self):
		return "SCMD "+str(self._position)+" "+str(self._cell_idx)

class SingleConditionData:

	_scmd = -1 #an array of SingleCellMovieData
	_condition_label = -1
	_nframes = -1

	def __init__(self,scmd,condition_label,nframes):
		self._scmd = scmd
		self._nframes = nframes
		self._condition_label = condition_label

	'''
	def plot(self,tp,filter_):
		combined = []
		for e in self._scmd:
			ts = e.get_time_series()
			if filter_(ts,e._position,e._cell_idx):
				continue
			ts = tp.transform(ts)
			plt.figure()
			plt.plot(ts)
			plt.xlabel('Time [1Frame = 10 mins]')
			plt.ylabel('Fold Change FRET/CFP EKAREV')
			title_ = self._condition_label+" "+str(e._position)+" "+str(e._cell_idx)
			plt.title(title_)
			plt.tight_layout()
			plt.savefig("C:\\Users\\gajduk\\Desktop\\figs\\"+title_+".png")
			plt.close()
	'''

	def __repr__(self):
		return "SCSFD"+str(self._condition_label)

class Dataset:

	_scd = -1 #an array of SingleConditionData
	_nframes = -1
	_frame_length_in_minutes = -1

	def __init__(self,scd,nframes,frame_length_in_minutes):
		self._scd = scd
		self._nframes = nframes
		self._frame_length_in_minutes = frame_length_in_minutes
