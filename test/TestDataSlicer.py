from nose.tools import assert_equals, assert_true, assert_raises
from DataSlicer import DataSlicer

class TestSliceData:
	def setup(self):
		self.window = 1
		self.ts_index = 0
		self.label_dict = {1:0,2:1}
		self.zero_slice_lines = [[100],[200],[300],[400],[500],[600]]
		self.one_slice_lines = [[100],[500],[700],[1100]]
		self.two_slice_lines = [[100],[500],[700],[61100],[61500],[61700],[62100]]
		self.three_slice_lines = [[100],[500],[700],[61100],[61500],[61700],[122100],[122700],[123100]]

	def test_slice_data_with_zero_slice_lines(self):
		ds = DataSlicer(self.window, self.ts_index)
		res = ds.sliceData(self.zero_slice_lines, self.label_dict)
		assert_equals(len(res), 0)

	def test_slice_data_with_one_slice_lines(self):
		ds = DataSlicer(self.window, self.ts_index)
		res = ds.sliceData(self.one_slice_lines, self.label_dict)
		assert_equals(len(res), 1)
		assert_equals(len(res[0]), 3)
		assert_equals(len(res[0][0]), 3)
		assert_equals(res[0][1], 0)
		assert_equals(res[0][2], 0)

	def test_slice_data_with_two_slice_lines(self):
		ds = DataSlicer(self.window, self.ts_index)
		res = ds.sliceData(self.two_slice_lines, self.label_dict)
		assert_equals(len(res), 2)
		assert_equals(len(res[1][0]), 3)
		assert_equals(res[1][1], 1)
		assert_equals(res[1][2], 61000)

	def test_slice_data_with_three_slice_lines(self):
		ds = DataSlicer(self.window, self.ts_index)
		res = ds.sliceData(self.three_slice_lines, self.label_dict)
		assert_equals(len(res), 3)
		assert_equals(len(res[2][0]), 2)
		assert_equals(res[2][1], 1)
		assert_equals(res[2][2], 122000)