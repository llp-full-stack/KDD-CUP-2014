import csv
from datetime import datetime

fin = open("outcomes.csv/outcomes.csv", "r")
reader = csv.reader(fin)

dict = {}

reader.next()

for row in reader:
	if row[1] == 't':
		value = 1
	else:
		value = 0
	dict[row[0]] = [value, 0]

fin.close()

fin = open("projects.csv/projects.csv", "r")
reader = csv.reader(fin)
reader.next()

for row in reader:
	if row[0] in dict:
		dict[row[0]][1] = datetime.strptime(row[-1], "%Y-%m-%d")

fin.close()

sorted_data = sorted(dict.viewitems(), lambda l, r: ((l[1][1] < r[1][1]) and -1) or ((l[1][1] == r[1][1]) and 0) or 1)

cnt = 0
t_cnt = 0

for item in sorted_data:
	cnt += 1
	if item[1][0] == 1:
		t_cnt += 1
	
	if cnt % 10000 == 0:
		print "%d exciting cases in the first %d cases" % (t_cnt, cnt)
		print item

print "%d exciting cases in the total %d cases" % (t_cnt, cnt)

