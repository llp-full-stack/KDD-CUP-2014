import random

random.seed()

fin = open("training.csv", "r")
fout = open("shuffled_training.csv", "w")

lst = fin.readlines()

tot = len(lst)

for i in xrange(tot - 1):
	rand = random.randint(i, tot-1)
	lst[i], lst[rand] = lst[rand], lst[i]

for str in lst:
	fout.write(str)


fin.close()
fout.close()

