import os

HOME = os.path.dirname(os.path.abspath(__file__))+"\\.."
FIGURES = HOME+"\\figures\\"
DATA = HOME+"\\data\\"
STACKS = 'E:\\hke3 11_11_16\\hke3 longtime\\'
TRACKS = 'E:\\hke3 11_11_16\\tracks temp\\'

def get_manual_boundaries():
	res = {}
	with open(DATA+'complete_res.txt', 'r') as pin:
		for line in pin:
			s_line = line.split()
			s_pos = s_line[0]
			cell_idx = int(s_line[1])
			try:
				start_t = int(s_line[2])
				end_t = int(s_line[3])
				res[s_pos, cell_idx] = (start_t, end_t)
			except:
				pass
	return res
