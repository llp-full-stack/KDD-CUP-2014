import csv

fin = open("submission_cmp.csv", "r")
reader = csv.reader(fin)

prev = -1

for row in reader:
	now = eval(row[1])
	if prev > now:
		print row
	prev = now

print "done"


fin.close()
