from parse_cell_profiler_output import DataReaderAndParser, HkeReaderBatch1

condition_ranges_longtime_batch2 = {1: "0 pg EGF", 10: "10 pg EGF", 20: "50 pg EGF", 30: "200 pg EGF"}
n_frames_batch2 = 257
frame_length_in_minutes_batch2 = 10
condition_ranges_longtime_batch3 = {1: "0 pg EGF", 15: "10 pg EGF", 40: "50 pg EGF", 65: "200 pg EGF"}
n_frames_batch3 = 198
frame_length_in_minutes_batch3 = 5


def getDataset(dataset_alias):
	'''
	:param dataset_alias: possible values are "hke3_batch1", "mdck_batch2" and "mdck_batch3"
	:return: a datasets.dataset object, or None if the dataset could not be found
	'''
	dataset = None
	if dataset_alias == "hke3_batch1":
		dataset = HkeReaderBatch1().read()
	elif dataset_alias == "batch2":
		dataset = DataReaderAndParser(condition_ranges_longtime_batch2,
		                              nframes=n_frames_batch2,
		                              frame_length_in_minutes=frame_length_in_minutes_batch2,
		                              file="""results 11_08_2016\\A1_Longtime_Cells.csv""").read()
	elif dataset_alias == "batch3":
		dataset = DataReaderAndParser(condition_ranges_longtime_batch3,
		                              nframes=n_frames_batch3,
		                              frame_length_in_minutes=frame_length_in_minutes_batch3,
		                              file="""real_weekend_Cells.csv""").read()
	else:
		print "ERROR: DATASET NOT FOUND" + dataset_alias
	return dataset
