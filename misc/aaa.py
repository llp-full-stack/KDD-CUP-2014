import os
import csv


for file in os.listdir("./"):
	print file
	if file[-3:] != "csv":
		continue
	fin = open(file, "r")
	reader = csv.reader(fin)
	for i in xrange(3):
		print reader.next()

	fin.close()


