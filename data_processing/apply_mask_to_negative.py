import os

mask_file = open("training_negative_mask.txt", "r")

mask = []
for line in mask_file:
	mask.append(eval(line))

mask_file.close()

print len(mask)
print mask.count(1)

file_list = os.listdir("training_negative/")

os.system("mkdir -p training_negative_masked/")

for file in file_list:
	print file

	input = open("training_negative/" + file, "r")
	output = open("training_negative_masked/" + file, "w")
	
	for i, line in enumerate(input):
		if mask[i] == 1:
			output.write(line)

	input.close()
	output.close()
