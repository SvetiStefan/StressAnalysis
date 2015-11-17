from nose.tools import assert_equals, assert_raises
from RawFeatureReader import RawFeatureReader

class TestInit:
	def setup(self):
		self.good_features = {'ts':1, 'gsr':-3, 'hr':-2}
		self.bad_features = {'a':-1, 'b':-2}

	def test_init_without_ts_in_features(self):
		assert_raises(LookupError, RawFeatureReader, self.bad_features)

	def test_init_with_right_feature_numbers(self):
		rfr = RawFeatureReader(self.good_features)
		assert_equals(len(rfr.rawFeatureNames()), 3)

	def test_init_ts_should_be_the_first_feature(self):
		rfr = RawFeatureReader(self.good_features)
		assert_equals(rfr.rawFeatureNames()[0], 'ts')

class TestReadRawFeatures:
	def setup(self):
		self.features = {'ts':0, 'gsr':1, 'hr':2}
		self.good_lines = ['ts,gsr,hr','1.1,1.2,1.3','2.1,2.2,2.3']
		self.bad_lines = ['asdf,asdf,asd','fg,we,fas','asdf,asdf,fd']
		self.good_lines_n_bad_lines = ['ts,gsr,hr','1.1,1.2,1.3','2.1,-.']

	def test_read_raw_features_with_good_lines(self):
		rfr = RawFeatureReader(self.features)
		features, lines = rfr.readRawFeatures(self.good_lines)
		assert_equals(len(lines), 2)
		assert_equals([lines[0][features['ts']],lines[0][features['gsr']],lines[0][features['hr']]], [1.1,1.2,1.3])
		assert_equals([lines[1][features['ts']],lines[1][features['gsr']],lines[1][features['hr']]], [2.1,2.2,2.3])

	def test_read_raw_features_with_good_lines_n_bad_lines(self):
		rfr = RawFeatureReader(self.features)
		features, lines = rfr.readRawFeatures(self.good_lines_n_bad_lines)
		assert_equals(len(lines), 1)
		assert_equals([lines[0][features['ts']],lines[0][features['gsr']],lines[0][features['hr']]], [1.1,1.2,1.3])

	def test_read_raw_features_with_bad_lines(self):
		rfr = RawFeatureReader(self.features)
		features, lines = rfr.readRawFeatures(self.bad_lines)
		assert_equals(len(lines), 0)


