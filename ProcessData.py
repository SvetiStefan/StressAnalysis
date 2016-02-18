import numpy as np

math_data = ['ShimmerData_Elisa_math.csv', 'ShimmerData_Emma_math.csv', 
	'ShimmerData_Haisheng_math.csv', 'ShimmerData_Issy_Math.csv', 
	'ShimmerData_May_Math.csv', 'ShimmerData_Sethu_math.csv']

# math_data = ['ShimmerData_Elisa_math.csv']

math_stress = {1:0,2:1,3:0,4:1,5:0,6:1}

ts_index = 1
hr_index = -2
gsr_index = -3
window = 60

training = []

def getRawFeature(line):
	items = line.strip().split(',')
	try:
		ts = float(items[ts_index])
		heart_rate = int(items[hr_index])
		gsr_val = float(items[gsr_index])
		items[ts_index] = ts
		items[hr_index] = heart_rate
		items[gsr_index] = gsr_val 
		return items
	except:
		return None

def genFeature(data, label, start):
	first_gsr = data[0][gsr_index]
	first_gsr_time = data[0][ts_index]
	last_gsr = data[-1][gsr_index]
	last_gsr_time = data[-1][ts_index]
	gsr_derivative = (last_gsr - first_gsr) * 1000.0 /(last_gsr_time - first_gsr_time)
	gsrs =[line[gsr_index] for line in data]
	gsr_std = np.std(gsrs)
	gsr_integral = 0
	last = start
	for line in data:
		gsr_integral += (line[ts_index] - last) * line[gsr_index] / 1000
		last = line[ts_index]
	training.append([last_gsr, gsr_derivative, gsr_integral, gsr_std, label])


def sliceDataNGenFeature(data, task, window):
	label_dict = None
	if task == 'math':
		label_dict = math_stress
	end = window * 1000
	current_slice = []
	for line in data:
		if line[ts_index] < end:
			current_slice.append(line)
		else:
			# finish of a slice
			window_middle_point = (end - (window * 1000)/2) / 1000
			minute = (window_middle_point / 60) + 1
			label = label_dict[minute] if minute in label_dict else 1
			genFeature(current_slice, label, end - window * 1000) # last 
			current_slice = []
			end += (window * 1000)


def handleMathData(math_data):
	for file_name in math_data:
		print file_name
		file_name = 'data/' + file_name
		processed_data = []
		with open(file_name, 'r') as f:
			for line in f:
				raw_features = getRawFeature(line)
				if raw_features is not None:
					processed_data.append(raw_features)
		sliceDataNGenFeature(processed_data, 'math', window)

def main():
	handleMathData(math_data)
	for line in training:
		print line

	from sklearn import linear_model
	from sklearn import cross_validation
	X = [line[:-1] for line in training]
	Y = [line[-1] for line in training]

	logreg = linear_model.LogisticRegression()

	scores = cross_validation.cross_val_score(logreg, X, Y, cv=3)
	acc = scores.mean()
	print acc


if __name__ == '__main__':
	main()