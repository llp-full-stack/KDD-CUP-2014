import csv


fin = open("is_exciting.csv", "r")
reader = csv.reader(fin)

reader.next()
s = set()

for row in reader:
	if row[0] in s:
		print "duplicate id:", row[0]

	s.add(row[0])

print len(s)
print "done"

fin.close()
