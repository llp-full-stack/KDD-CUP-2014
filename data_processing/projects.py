# Creates statistics and feature matrix from the given csv

import csv
import sys

# feature types:
# numeric:	treat the field as a number
# boolean:	treat the field as a boolean value, if the field has more than 2 possible values
#			each value is treated as a boolean feature
# hash:		number each possible value and use the hash value as the feature
# raw:		raw data, for project id
# none:		ignore the field	

feature_type_no = {"numeric": 0, "boolean": 1, "hash": 2, "raw": 3, "none": 4}
feature_type_name = ["numeric", "boolean", "hash", "raw", "none"]
maximum_category = 100		# the maximum number of features that is allowed to be created from one field

def getFile():
	if len(sys.argv) <= 1:
		print "[Error] no input file provided"
		sys.exit(1)
	
	name_part = sys.argv[1].rfind('.')
	if name_part == -1:
		name_part = len(sys.argv[1])
	name_part = sys.argv[1][:name_part]
	
	if len(sys.argv) <= 2:
		out = name_part + ".out"
	else:
		out = sys.argv[2]

	if len(sys.argv) <= 3:
		report_out = name_part + "_report.txt"
	else:
		report_out = sys.argv[3]

	return sys.argv[1], out, report_out 


def statFields(file_name):
	fin = open(file_name, "r")
	reader = csv.reader(fin)
	
	header = reader.next()
	dicts = []
	for field_name in header:
		dicts.append([field_name, {}])

	for data in reader:
		for i, datum in enumerate(data):
			if datum in dicts[i][1]:
				dicts[i][1][datum] += 1
			else:
				dicts[i][1][datum] = 1

	fin.close()

	return dicts

def isNumber(str):
	if str == '':
		return True
	try:
		float(str)
		return True
	except ValueError:
		return False

def getDefaultFeatureType(dict):
	length = len(dict)
	if length <= 1:
		return feature_type_no["none"]
	elif length == 2:
		return feature_type_no["boolean"]
	else:
		if reduce(lambda isnumber, key: isnumber and isNumber(key), dict.viewkeys(), True):
			return feature_type_no["numeric"]
		else:
			if length <= maximum_category:
				return feature_type_no["boolean"]
			else:
				return feature_type_no["none"]
	
	return feature_type_no["none"]

def printFeatureTypeOfSingleField(i, field):
	print str(i) + ":", field[0], field[2], feature_type_name[field[3]]
	if field[2] <= 10:
		print field[1]

def printFeatureTypesOfFields(fields):
	print "feature types:"
	for i, field in enumerate(fields):
		printFeatureTypeOfSingleField(i, field)
	print

def printStatFeatureTypeHelpMessage():
	print 'Enter "help" to print this help message'
	print 'Enter "print all" to print all fields again'
	print 'Enter "print i" to print the ith field'
	print 'Enter "printset i" to print the ith field\'s key set '
	print 'Enter "modify i feature_type" to change feature type of i'
	print 'Enter "done" to continue'
	print

def askForStatFeatureType(fields):

	map(lambda field: field.extend([len(field[1]), getDefaultFeatureType(field[1])]), fields)

	printFeatureTypesOfFields(fields)
	printStatFeatureTypeHelpMessage()

	while True:
		command = raw_input().split(" ")
		
		if command[0] == "help":
			printFeatureTypeHelpMessage()

		elif command[0] == "print":
			if len(command) < 2:
				print 'insufficient arguments'
				continue
			if command[1] == "all":
				printFeatureTypesOfFields(fields)
			else:
				if not command[1].isdigit():
					print 'print followed by neither "all" nor a number'
					continue
				id = eval(command[1])
				if id >= len(fields) or id < 0:
					print 'index out of bound, index should be in range [0, %d)' % len(fields)
					continue
				
				printFeatureTypeOfSingleField(id, fields[id])

		elif command[0] == "modify":
			if len(command) < 3:
				print 'insufficient arguments'
				continue

			if not command[1].isdigit():
				print 'modify followed not by a number'
				continue
			id = eval(command[1])
			if (id >= len(fields) or id < 0):
				print 'index out of bound, index should be in range [0, %d)' % len(fields)
				continue

			if not command[2] in feature_type_no:
				print 'unrecoginized feature type'
				continue

			fields[id][3] = feature_type_no[command[2]]
			printFeatureTypeOfSingleField(id, fields[id])
		elif command[0] == "printset":
			if len(command) < 2:
				print 'insufficient arguments'
				continue

			if not command[1].isdigit():
				print 'printset followed not by a number'
				continue
			id = eval(command[1])
			if (id >= len(fields) or id < 0):
				print 'index out of bound, index should be in range [0, %d)' % len(fields)
				continue
			print fields[id][1]

		elif command[0] == "done":
			break

		else:
			print "unrecognized command"

	return map(lambda field: field[3], fields)

def raw_feature(item, additional):
	return item

def numeric_feature(item, additional):
	if item == '':
		return 0.0
	return float(item)

def hash_feature(item, additional):
	return additional[item]

def boolean_feature(item, additional):
	if item == additional:
		return 1
	else:
		return 0


def getAdditionalFeatureInfo(fields, feature_type, report_file):
	report_out = open(report_file, "w")

	additional_info = []
	func = []
	index = []
	for i, type in enumerate(feature_type):
		if type == 0:		# numeric			
			additional_info.append(None)
			func.append(numeric_feature)
			index.append(i)

			report_out.write("feature " + str(len(func) - 1) + ": ")
			report_out.write("type = numeric ")
			report_out.write("field_name = " + fields[i][0])
			
			report_out.write("\n")
		
		if type == 1:		# boolean
			if len(fields[1]) == 2:		# 2 values
				additional_info.append(fields[i][1].keys()[0])
				func.append(boolean_feature)
				index.append(i)

				report_out.write("feature " + str(len(func) - 1) + ": ")
				report_out.write("type = boolean (2 values) ")
				report_out.write("field_name = " + fields[i][0])
				report_out.write(" true = " + additional_info[-1])
				report_out.write("\n")

			else:						# multiple values
				for key in fields[i][1].viewkeys():
					additional_info.append(key)
					func.append(boolean_feature)
					index.append(i)
					
					report_out.write("feature " + str(len(func) - 1) + ": ")
					report_out.write("type = boolean (> 2 values) ")
					report_out.write("field_name = " + fields[i][0])
					report_out.write(" true = " + key)
					report_out.write("\n")

		if type == 2:		# hash
			print fields[i][0], "hash:"
			print fields[i][1]
		
			print "need manually assign? (y/n) ",
			need_input = raw_input()
			if need_input[0] == "y":

				hashdict = {}
				for field in fields[i][1].viewkeys():
					print field + ":",
					n = input()
					hashdict[field] = n
			else:
				hashdict = {}
				cnt = 0
				for field in fields[i][1].viewkeys():
					hashdict[field] = cnt
					cnt += 1

			additional_info.append(hashdict)
			func.append(hash_feature)
			index.append(i)

			report_out.write("feature " + str(len(func) - 1) + ": ")
			report_out.write("type = hash ")
			report_out.write("field_name = " + fields[i][0])
			report_out.write("\n")
			
			for item in hashdict.viewitems():
				print item

		if type == 3:		# raw
			additional_info.append(None)
			func.append(raw_feature)
			index.append(i)

			report_out.write("feature " + str(len(func) - 1) + ": ")
			report_out.write("type = raw ")
			report_out.write("field_name = " + fields[i][0])
			report_out.write("\n")


	report_out.close()

	return additional_info, func, index

def process(input_file_name, output_file_name, report_file_name, fields, feature_type):
	additional_info, func, index = getAdditionalFeatureInfo(fields, feature_type, report_file_name)

	fin = open(input_file_name, "r")
	fout = open(output_file_name, "w")
	reader = csv.reader(fin)
	writer = csv.writer(fout, delimiter = ' ')
	reader.next()

	for raw_row in reader:
		row = []
		for info, f, i in zip(additional_info, func, index):
			row.append(f(raw_row[i], info))
		writer.writerow(row)

	fin.close()
	fout.close()

def main():
	input_file_name, output_file_name, report_file_name = getFile()

	field_stat = statFields(input_file_name)
	
	feature_type = askForStatFeatureType(field_stat)

	process(input_file_name, output_file_name, report_file_name, field_stat, feature_type)

if __name__ == "__main__":
	main()

