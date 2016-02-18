import math
from nose.tools import assert_equals, assert_true, assert_raises
from FeatureGenerator import FeatureGenerator

class TestGenFeaturesForOne:
	def setup(self):
		self.feature_dict = {'ts':0,'gsr':1,'hr':2}
		self.ts_index = self.feature_dict['ts']
		self.simple_data = [[1, 50, 70], [2, 50, 80]]
		self.normal_data = [[1, 50, 70], [2, 60, 80], [3, 70, 80], [4, 80, 90]]
		
	def test_gen_feature_for_static_feature(self):
		fg = FeatureGenerator(self.feature_dict)
		f_index = self.feature_dict['gsr']
		res = fg.genFeaturesForOne(self.simple_data, self.ts_index, f_index, 0)
		assert_equals(res, [50.0, 0.0, 0.0, 0.1])

	def test_gen_feature_for_dynamic_feature(self):
		fg = FeatureGenerator(self.feature_dict)
		f_index = self.feature_dict['hr']
		res = fg.genFeaturesForOne(self.simple_data, self.ts_index, f_index, 0)
		assert_equals(res, [75.0, 5.0, 10000, 0.15])

	def test_gen_feature_on_normal_data(self):
		fg = FeatureGenerator(self.feature_dict)
		f_index = self.feature_dict['gsr']
		res = fg.genFeaturesForOne(self.normal_data, self.ts_index, f_index, 0)
		assert_equals(res, [65.0, math.sqrt(125.0), 10000.0, 0.26])
		f_index = self.feature_dict['hr']
		res = fg.genFeaturesForOne(self.normal_data, self.ts_index, f_index, 0)
		assert_equals(res, [80.0, math.sqrt(50.0), 20*1000.0/3, 0.32])


class TestGenFeatures(object):
	def setup(self):
		self.feature_dict = {'ts':0,'gsr':1,'hr':2}
		self.simple_data = [[[[1, 50, 70], [2, 50, 80]], 0, 1]]
		self.normal_data = [[[[1, 50, 70], [2, 60, 80], [3, 70, 80], [4, 80, 90]], 0, 1]]

	def test_gen_feature_for_one_raw_feature(self):
		fg = FeatureGenerator(self.feature_dict)
		res = fg.genFeatures(self.simple_data, ['gsr'])
		assert_equals(res, [[50.0, 0.0, 0.0, 0.1, 1]])

	def test_gen_feature_for_two_raw_features(self):
		fg = FeatureGenerator(self.feature_dict)
		res = fg.genFeatures(self.simple_data, ['gsr', 'hr'])
		assert_equals(res, [[50.0, 0.0, 0.0, 0.1, 75.0, 5.0, 10000, 0.15, 1]])

	def test_gen_feature_on_normal_data(self):
		fg = FeatureGenerator(self.feature_dict)
		res = fg.genFeatures(self.normal_data, ['gsr', 'hr'])
		assert_equals(res, [[65.0, math.sqrt(125.0), 10000.0, 0.26, 80.0, math.sqrt(50.0), 20*1000.0/3, 0.32, 1]])
		
