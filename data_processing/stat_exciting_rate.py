import csv

training_cnt = 619326
positive_cnt = 36710
negative_cnt = 582616
test_cnt = 44772
feature_range = [range(69,97), range(97, 105)]
start_id = 533


def calc_exciting_rate(feature_range, new_id):
	cnt = [0] * len(feature_range)

	positive_category = [-1] * positive_cnt
	negative_category = [-1] * negative_cnt
	test_category = [-1] * test_cnt

	for i, feature_id in enumerate(feature_range):
		fin = open("training_positive/%d.csv" % feature_id, "r")
	
		for case_id, line in enumerate(fin):
			if eval(line) == 1:
				cnt[i] += 1
				positive_category[case_id] = i

		fin.close()

		fin = open("training_negative/%d.csv" % feature_id, "r")

		for case_id, line in enumerate(fin):
			if eval(line) == 1:
				negative_category[case_id] = i

		fin.close()

		fin = open("test/%d.csv" % feature_id, "r")

		for case_id, line in enumerate(fin):
			if eval(line) == 1:
				test_category[case_id] = i

		fin.close()

	exciting_rate = [float(cnt[i]) / training_cnt for i in xrange(len(feature_range))]

	print exciting_rate

	fout = open("training_positive/%d.csv" % new_id, "w")

	for i in positive_category:
		fout.write(str(exciting_rate[i]) + "\n")

	fout.close()

	fout = open("training_negative/%d.csv" % new_id, "w")

	for i in negative_category:
		fout.write(str(exciting_rate[i]) + "\n")

	fout.close()

	fout = open("test/%d.csv" % new_id, "w")

	for i in test_category:
		fout.write(str(exciting_rate[i]) + "\n")
	
	fout.close()

for i in xrange(len(feature_range)):
	calc_exciting_rate(feature_range[i], start_id + i)

