fin = open("shuffled_training.csv", "r")

_66_cnt = 0

ln = 0
for line in fin:
	ln += 1
	row = line.split()
	for i in xrange(4, len(row)):
		index = eval(row[i].split(':')[0])
		if (index == 524):
			print ln, (row[i].split(':')[1])
			_66_cnt += 1
		if (index >= 524):
			break
			
print _66_cnt

fin.close()
