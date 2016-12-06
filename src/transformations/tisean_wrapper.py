from os import chdir,getcwd
from subprocess import Popen, PIPE, STDOUT

import numpy as np
import matplotlib.pylab as plt

tisean_path = "C:\\Users\\gajduk\\Tisean_3_0_0\\bin\\"

def simple_example_of_noise_reduction():
	x = np.linspace(0,7,100)

	test_data_original = np.sin(x)

	test_data_with_noise = test_data_original+np.random.normal(0,.3,len(x))
	plt.plot(x,test_data_original)
	plt.plot(x,test_data_with_noise)

	chdir(tisean_path)

	p = Popen(["ghkss"], stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)    
	test_data_recovered_string = p.communicate(input=('\n'.join([str(e) for e in test_data_with_noise])+'\n'))[0]

	test_data_recovered = []
	for line in test_data_recovered_string.split('\n'):
		val = -1
		try:
			val = float(line)
			test_data_recovered.append(val)
		except:
			pass

	plt.plot(x,test_data_recovered)
	plt.legend(['original','added noise','denoised'])
	plt.show()

def embeding_dimension(ts):
	command = "false_nearest -M1,4"
	cwd = getcwd()
	chdir(tisean_path)
	p = Popen(command.split(' '), stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)
	res_s = p.communicate(input=('\n'.join([str(e) for e in ts])+'\n'))[0]

	res = {}
	for line in res_s.split('\n'):
		val = -1
		s_line = line.split(' ')
		try:
			dim = int(s_line[0])
			val = float(s_line[1])
			res[dim] = val
		except:
			pass
	chdir(cwd)
	return res
	

class TiseanTransformation:

	def __init__(self,command):
		self._command = command

	def transform(self,ts):
		cwd = getcwd()
		chdir(tisean_path)
		p = Popen(self._command.split(' '), stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)
		res_s = p.communicate(input=('\n'.join([str(e) for e in ts])+'\n'))[0]
		chdir(cwd)
		res = []
		for line in res_s.split('\n'):
			val = -1
			try:
				val = float(line)
				res.append(val)
			except:
				pass
		res_filled_with_nans = []
		k = 0
		for i,e in enumerate(ts):
			if np.isnan(e):
				res_filled_with_nans.append(float('NaN'))
			else:
				res_filled_with_nans.append(res[k])
				k += 1
		return res_filled_with_nans

	def __str__(self):
		return "Tisean "+self._command

if __name__ == "__main__":
	simple_example_of_noise_reduction