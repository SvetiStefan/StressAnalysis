import numpy as np

class FeatureGenerator(object):
	"""
	    FeatureGenerator generates 4 features for each raw feature
	    including mean value, std value, derivate and integral.
	"""
	def __init__(self, feature_dict):
		self.__feature_dict = feature_dict
		self.__ts_index = feature_dict['ts']
		self.__features = []

		
	def genFeaturesForOne(self, lines, ts_index, f_index, st_time):
		raw_values = [line[f_index] for line in lines]
		ts_values = [st_time] + [line[st_time] for line in lines]
		ts_intervels = [ts_values[i] - ts_values[i-1] for i in range(1,len(ts_values))]
		avg_value = np.mean(raw_values)
		std_value = np.std(raw_values)
		derivate = (lines[-1][f_index] - lines[0][f_index]) * 1000.0 / (lines[-1][ts_index] - lines[0][ts_index])
		integral = sum([a*b for a,b in zip(raw_values,ts_intervels)]) / 1000.0 # ts is in milli second
		return [avg_value, std_value, derivate, integral]

	def genFeatures(self, raw_dataset, raw_features):
		for one_entry in raw_dataset:
			lines = one_entry[0]
			feature_line = []
			for key in raw_features:
				f_index = self.__feature_dict[key]
				feature_line += self.genFeaturesForOne(lines, self.__ts_index, f_index, one_entry[1])
			feature_line.append(one_entry[2])
			self.__features.append(feature_line)
		return self.__features


		