function [test, training, training_outcome, assessment, assessment_outcome] = load_data
	rng('shuffle');


	% Load data
	test = load_data_from('test/');
	training = load_data_from('training_negative/');
	training_positive = load_data_from('training_positive/');

	training_outcome = [zeros(size(training, 1), 1) ; ones(size(training_positive, 1), 1)];
	training = [training ; training_positive];

	% Shuffle data
	p = randperm(size(training, 1));

	training = training(p, :);
	training_outcome = training_outcome(p, :);

	% split training and assessment sets
	num_of_training = floor(size(training, 1) * 0.800000);
	assessment = training(num_of_training+1:size(training,1), :);
	assessment_outcome = training_outcome(num_of_training+1:size(training,1), :);
	training = training(1:num_of_training,:);
	training_outcome = training_outcome(1:num_of_training, :);

end


function result = load_data_from(folder)

	% load data
	data_151 = dlmread(strcat(folder, '151.csv'));
	data_150 = dlmread(strcat(folder, '150.csv'));
	data_153 = dlmread(strcat(folder, '153.csv'));
	data_152 = dlmread(strcat(folder, '152.csv'));
	data_157 = dlmread(strcat(folder, '157.csv'));
	data_156 = dlmread(strcat(folder, '156.csv'));
	data_158 = dlmread(strcat(folder, '158.csv'));
	data_148 = dlmread(strcat(folder, '148.csv'));
	data_149 = dlmread(strcat(folder, '149.csv'));
	data_524 = dlmread(strcat(folder, '524.csv'));
	data_525 = dlmread(strcat(folder, '525.csv'));
	data_67 = dlmread(strcat(folder, '67.csv'));
	data_68 = dlmread(strcat(folder, '68.csv'));


	% initialize result
	result = zeros(size(data_68, 1), 13);

	% arithmetic ops
	result(:, 1) = ones(size(data_68, 1), 1);
	result(:, 2) = data_525;
	result(:, 3) = data_156;
	result(:, 4) = data_157;
	result(:, 5) = exp(data_148);
	result(:, 6) = data_524 .* data_149;
	result(:, 7) = data_524 .* data_150;
	result(:, 8) = data_524 .* data_151;
	result(:, 9) = data_524 .* data_152;
	result(:, 10) = data_524 .* data_153;
	result(:, 11) = data_158;
	result(:, 12) = data_67;
	result(:, 13) = data_68;


end
