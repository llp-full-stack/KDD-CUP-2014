import csv
from datetime import datetime

timestr = "2012-2-25"
timepoint = datetime.strptime(timestr, "%Y-%m-%d")

fout = open("project_id_after_%s.txt" % timestr, "w")
fin = open("projects.csv/projects.csv", "r")
reader = csv.reader(fin)
reader.next()


for row in reader:
	if (datetime.strptime(row[-1], "%Y-%m-%d") > timepoint):
		fout.write(row[0] + "\n")

fin.close()
fout.close()
