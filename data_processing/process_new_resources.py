import csv
import os

def create_resources_feature_dict():
	features = {}

	fin = open("new_resources.csv", "r")
	reader = csv.reader(fin)

	for row in reader:
		delim_pos = row.index("-1")
		features[row[0]] = [row[1:delim_pos], row[delim_pos+1:-1], row[-1]]

	fin.close()
	
	return features


features = create_resources_feature_dict()

def print_features(id_file, folder):
	fin = open(id_file, "r")

	fout = [0] * 525
	for i in xrange(160, 525):
		fout[i] = open("%s/%d.csv" % (folder, i), "w")

	for id in fin:
		if id[-1] == "\n":
			id = id[:-1]
		if id in features:
			feature = features[id]
		else:
			feature = [ [], [], '0' ]

		for i in xrange(160, 517):
			if str(i - 160) in feature[0]:
				fout[i].write("1\n")
			else:
				fout[i].write("0\n")
		for i in xrange(517, 524):
			if str(i - 517) in feature[1]:
				fout[i].write("1\n")
			else:
				fout[i].write("0\n")
		fout[524].write(feature[2] + "\n")

	for i in xrange(160, 525):
		fout[i].close()
	fin.close()


print_features("training_negative_id.csv", "training_negative")
print_features("test_report.txt", "test")
print_features("training_positive_id.csv", "training_positive")


