import csv

training = open("training.csv", "r")
training_seq = open("training_report.txt", "r")

positive = open("training_positive.csv", "w")
positive_seq = open("training_positive_id.csv", "w")
negative = open("training_negative.csv", "w")
negative_seq = open("training_negative_id.csv", "w")


positive_cnt = 0
negative_cnt = 0

for line in training:
	id = training_seq.readline()
	if line[0] == '0':
		negative_cnt += 1
		negative.write(line)
		negative_seq.write(id)
	else:
		positive_cnt += 1
		positive.write(line)
		positive_seq.write(id)

print positive_cnt, negative_cnt


positive.close()
negative.close()
positive_seq.close()
negative_seq.close()

training.close()
training_seq.close()

