import os

dir = "training_negative_masked/"

file_list = os.listdir(dir)

os.system("rm log")

for file in file_list:
	os.system("echo %s >> log" % file)

	os.system("python count_line.py %s%s >> log" % (dir, file) )
