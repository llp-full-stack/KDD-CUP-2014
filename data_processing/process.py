import os
import csv

def read_one_config(file_name, feature_start):
	feature_cnt = feature_start[-1]
	del feature_start[-1]

	cnt = 0
	fin = open(file_name, "r")
	for row_str in fin.readlines():
		row = row_str.split(" ")
		feature_start.append(feature_cnt)

		if row[0] == "boolean" and eval(row[1]) > 2:
			feature_cnt += eval(row[1])
		elif row[0] == "none":
			feature_cnt += 0
		else:
			feature_cnt += 1
		
		cnt += 1

	feature_start.append(feature_cnt)

	return feature_start, cnt

def read_config():
	feature_start, p_cnt = read_one_config("projects_config", [0])
	feature_start, d_cnt  = read_one_config("donation_config", feature_start)
	feature_start, r_cnt  = read_one_config("resources_config", feature_start)

	return feature_start, p_cnt, d_cnt, r_cnt 

def create_sets(feature, p_cnt, d_cnt, r_cnt):
	training = {}
	test = {}

	fin = open("training_projects.out", "r")
	reader = csv.reader(fin, delimiter = ' ')

	now = 0
	for row in reader:
		training[row[0]] = []
		for i in xrange(p_cnt):
			value = eval(row[i + 1])

			if feature[now + i] == feature[now + i + 1]:
				continue
			
			if feature[now + i] + 1 < feature[now + i + 1]:
				training[row[0]].append((feature[now + i] + value, 1))
			else:
				if value != 0:
					training[row[0]].append((feature[now+i], value))

	fin.close()

	fin = open("test_projects.out", "r")
	reader = csv.reader(fin, delimiter = ' ')

	now = 0 
	for row in reader:
		test[row[0]] = []
		for i in xrange(p_cnt):
			value = eval(row[i + 1])

			if feature[now + i] == feature[now + i + 1]:
				continue

			if feature[now + i] + 1 < feature[now + i + 1]:
				test[row[0]].append((feature[now + i] + value, 1))
			else:
				if value != 0:
						test[row[0]].append((feature[now+i], value))

	fin.close()

	fin = open("donation_data.csv", "r")
	reader = csv.reader(fin)
	
	reader.next()

	now = p_cnt
	for row in reader:
		for i in xrange(d_cnt):
			value = eval(row[i + 1])

			if feature[now + i] == feature[now + i + 1]:
				continue
			
			if feature[now + i] + 1 < feature[now + i + 1]:
				if row[0] in training:
					training[row[0]].append((feature[now+i] + value, 1))
				else:
					test[row[0]].append((feature[now+i] + value, 1))
			else:
				if value != 0:
					if row[0] in training:
						training[row[0]].append((feature[now+i], value))
					else:
						test[row[0]].append((feature[now+i], value))

	fin.close()

	fin = open("resources.csv", "r")
	reader = csv.reader(fin)
	
	now = p_cnt+d_cnt
	for row in reader:
		for i in xrange(r_cnt):
			value = eval(row[i + 1])

			if feature[now + i] == feature[now + i + 1]:
				continue

			if feature[now + i] + 1 < feature[now + i + 1]:
				if row[0] in training:
					training[row[0]].append((feature[now+i] + value, 1))
				else:
					test[row[0]].append((feature[now+i] + value, 1))
			else:
				if value != 0:
					if row[0] in training:
						training[row[0]].append((feature[now+i], value))
					else:
						test[row[0]].append((feature[now+i], value))

	fin.close()

	fin = open("outcomes.csv", "r")
	reader = csv.reader(fin)

	for row in reader:
		training[row[0]].append(eval(row[1]))

	fin.close()
	return training, test

def print_set(filename, report_name, set, hasOutcome):

	fout = open(filename, "w")
	report_out = open(report_name, "w")
	writer = csv.writer(fout, delimiter = ' ')

	for item in set.viewitems():
		report_out.write(item[0])

		row = []
		non_zero_cnt = 0
		if hasOutcome:
			row.append(str(item[1][-1]))
			row.extend([str(len(item[1]) -1), "0", "0"])
			non_zero_cnt = len(item[1]) - 1
		else:
			row.extend([str(len(item[1])), "0", "0"])
			non_zero_cnt = len(item[1])

		for i in xrange(non_zero_cnt):
			row.append("%d:%d" % item[1][i] )

		writer.writerow(row)

	fout.close()

def main():
	feature, p_cnt, d_cnt, r_cnt = read_config()		# reads configs and calculate feature count
	
	print feature[0:p_cnt]

	print feature[p_cnt:p_cnt + d_cnt]

	print feature[p_cnt+d_cnt:]

	print p_cnt, d_cnt, r_cnt

	#training, test = create_sets(feature, p_cnt, d_cnt, r_cnt)		# creates the two sets

	#print_set("training.csv", "training_report.txt", training, True)
	#print_set("test.csv", "test_report.txt", test, False)


if __name__ == "__main__":
	main()

