import csv

id_set = set()

def load_to_set(id_set, filename):
	fin = open(filename, "r")

	for line in fin:
		if line[-1] == "\n":
			line = line[:-1]
		id_set.add(line)

	fin.close()


load_to_set(id_set, "training_negative_id.csv")

fin = open("new_resources.csv", "r")
reader = csv.reader(fin)

fout = open("missing_id.csv", "w")

for row in reader:
	if row[0] in id_set:
		id_set.remove(row[0])

for id in id_set:
	print id
	fout.write(id + "\n")

print "tot_missing_id_cnt =", len(id_set) 
fout.write("tot_missing_id_cnt = %d\n" % len(id_set))

fin.close()
fout.close()

