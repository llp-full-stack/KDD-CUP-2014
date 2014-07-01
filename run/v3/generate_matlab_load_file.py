
## parameters

HAS_CONSTANT_ITEM = True
ASSESSMENT_PERCENTAGE = 0.2


## generating load_data.m

fout = open("load_data.m", "w")

fout.write(
"""function [test, training, training_outcome, assessment, assessment_outcome] = load_data
	rng('shuffle');


	%% Load data
	test = load_data_from('test/');
	training = load_data_from('training_negative/');
	training_positive = load_data_from('training_positive/');

	training_outcome = [zeros(size(training, 1), 1) ; ones(size(training_positive, 1), 1)];
	training = [training ; training_positive];

	%% Shuffle data
	p = randperm(size(training, 1));

	training = training(p, :);
	training_outcome = training_outcome(p, :);

	%% split training and assessment sets
	num_of_training = floor(size(training, 1) * %f);
	assessment = training(num_of_training+1:size(training,1), :);
	assessment_outcome = training_outcome(num_of_training+1:size(training,1), :);
	training = training(1:num_of_training,:);
	training_outcome = training_outcome(1:num_of_training, :);

end

""" % (1 - ASSESSMENT_PERCENTAGE) )


data_column_set = set()
data_load_code = []
data_arith_code = []

fin = open("matlab_config", "r")

lineno = 0
if HAS_CONSTANT_ITEM:
	lineno += 1
	data_arith_code.append("")	# fill later

for line in fin:
	if line[-1] == '\n':
		line = line[:-1]
	lineno += 1

	lmarker = line.find('@');
	while lmarker != -1:
		rmarker = line.find('#', lmarker + 1)
		if rmarker == -1:
			break

		data_column_set.add(line[lmarker+1:rmarker])

		lmarker = line.find('@', rmarker + 1)

	
	data_arith_code.append("	result(:, %d) = %s;\n" % (lineno, line.replace('@', 'data_').replace('#', '') ));
	

for column_id in data_column_set:
	any_id = column_id
	data_load_code.append("\tdata_%s = dlmread(strcat(folder, '%s.csv'));\n" % (column_id, column_id) ) 

if HAS_CONSTANT_ITEM:
	data_arith_code[0] = "	result(:, 1) = ones(size(data_%s, 1), 1);\n" % any_id

data_arith_code = "".join(data_arith_code)
data_load_code = "".join(data_load_code)

fin.close()

fout.write(
"""
function result = load_data_from(folder)

	%% load data
%s

	%% initialize result
	result = zeros(size(data_%s, 1), %d);

	%% arithmetic ops
%s

end
""" % (data_load_code, any_id, lineno, data_arith_code)
)


fout.close()

