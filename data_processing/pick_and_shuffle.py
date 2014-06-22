import random

positive_cnt = 36710
positive_in_use_cnt = positive_cnt
negative_cnt = 582516
negative_in_use_cnt = 5 * positive_cnt

def do_shuffle(tot, cnt, input, input2):
	
	if cnt < tot:
		use = [0] * tot
		num = range(tot)
		for i in xrange(cnt):
			rand = random.randint(i, tot-1)
			num[i], num[rand] = num[rand], num[i]
			use[num[i]] = 1

	else:
		use = [1] * tot

        result = []
        result2 = []
	for i in xrange(tot):
		if use[i] == 1:
			result.append(input.readline())
			result2.append(input2.readline())
		else:
			input.readline()
			input2.readline()
			
	return result, result2

input = open("training_positive.csv", "r")
input2 = open("training_positive_id.csv", "r")

result, result2 = do_shuffle(positive_cnt, positive_in_use_cnt, input, input2)

input.close()
input2.close()

input = open("training_negative.csv", "r")
input2 = open("training_negative_id.csv", "r")

rt, rt2 = do_shuffle(negative_cnt, negative_in_use_cnt, input, input2)

result.extend(rt)
result2.extend(rt2)

input.close()
input2.close()

output = open("shuffled_training.csv", "w")
output2 = open("shuffled_training_id.csv", "w")

if len(result) > 0:
	for i in xrange(len(result) - 1):
		rand = random.randint(i, len(result) - 1)
		result[i], result[rand], result2[i], result2[rand] = result[rand], result[i], result2[rand], result2[i]
		
for i in xrange(len(result)):
	output.write(result[i])
	output2.write(result2[i])

output.close()
output2.close()

