import csv

id_set = set()

def load_to_set(id_set, filename):
	fin = open(filename, "r")

	for line in fin:
		if line[-1] == "\n":
			line = line[:-1]
		id_set.add(line)

	fin.close()

def remove_from_set(id_set, filename):
	fin = open(filename, "r")

	for line in fin:
		if line[-1] == "\n":
			line = line[:-1]
		id_set.discard(line)

	fin.close()

load_to_set(id_set, "project_id_after_2012-2-25.txt")
remove_from_set(id_set, "missing_id.csv")	# ids missing from new_resources.csv

mask_file = open("training_negative_mask.txt", "w")
id_file = open("training_negative_id.csv", "r")

for row in id_file:
	if row[-1] == "\n":
		row = row[:-1]
	if row in id_set:
		mask_file.write("1\n")
	else:
		mask_file.write("0\n")


id_file.close()
mask_file.close()

