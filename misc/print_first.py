import sys
import csv

fin = open(sys.argv[1], "r")
reader = csv.reader(fin)

n = eval(sys.argv[2])

header = reader.next()
print header

if n > 1:
	for i in xrange(n-1):
		print reader.next()

print len(header)

fin.close()

