import json
class RawFeatureReader(object):
	"""
	    RawFeatureReader read raw features from file
	    and convert it into the right format.
	"""
	def __init__(self, raw_feature_index):
		if 'ts' not in raw_feature_index:
			raise LookupError('ts not in raw features')
		self.__raw_feature_index = raw_feature_index
		self.__raw_features = ['ts']
		for key in self.__raw_feature_index:
			if key != 'ts':
				self.__raw_features.append(key)

	def rawFeatureNames(self):
		return self.__raw_features

	def splitFile(self, file_name):
		lines = None
		with open(file_name, 'r') as f:
			lines = f.readlines()
		return lines

	def readRawFeatures(self, lines):
		feature_lines = []
		for line in lines:
			items = line.strip().split(',')
			features = []
			try:
				for feature in self.__raw_features:
					features.append(float(items[self.__raw_feature_index[feature]]))
			except:
				continue
			feature_lines.append(features)
		feature_dict = {self.__raw_features[i]:i for i in range(len(self.__raw_features))}
		return feature_dict, feature_lines

	def readRawFeaturesFromFile(self, file_name):
		lines = self.splitFile(file_name)
		return self.readRawFeatures(lines)
				



