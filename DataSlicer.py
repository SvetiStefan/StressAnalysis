
class DataSlicer(object):
	"""
	    DataSlicer slice data file into slices. 
	    Each slice contains data in a window
	"""
	def __init__(self, window, ts_index):
		self.__w = window
		self.__t = ts_index
		self.__slices = []
		
	def sliceData(self, lines, label_dict):
		end = self.__w * 1000
		current_slice = []
		for line in lines:
			if line[self.__t] < end:
				current_slice.append(line)
			else:
				# finish of a slice
				window_middle_point = (end - (self.__w  * 1000)/2) / 1000
				minute = (window_middle_point / 60) + 1
				label = label_dict[minute] if minute in label_dict else 1
				self.__slices.append([current_slice, label, end - self.__w * 1000]) 
				# start a new slice
				current_slice = [line]
				while end < line[self.__t]:
					end += (self.__w * 1000)
		return self.__slices