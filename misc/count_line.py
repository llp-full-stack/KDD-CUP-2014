import sys

if len(sys.argv) < 2:
	exit()

input = open(sys.argv[1], "r")

print len(input.readlines())

input.close()

