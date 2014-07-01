function logistic_regression()
	training_set = dlmread('training_partial.csv');
	A = spconvert(training_set);
    A = full(A);
    [tm, tn] = size(A);
    A = [ones(tm, 1), A];
	y = dlmread('training_ans.csv');
	% now y is a row vector of 1 * m
	y = y';
    [A, CV, T, y, y_cv, y_t] = divide(A, y);
	% m is the total number of training datas
	% n is the number of features
	[m, n] = size(A);
	
    lambda = 2;
    function [f, g] = cost_function(x)
            % returns a vector of 1 * m
            hypo = sigmod(x, A);
            u = -y * log(hypo)' - (1 - y) * log(1 - hypo)';
            f = (u + lambda * (x * x') / 2) / m;
            g = ((hypo - y) * A  + lambda * x) / m;
    end
    
    AUC_result = 0;
    options = optimoptions('fminunc','GradObj','on');
    
    file_cnt = 0;
    while (lambda < 20)
        % x is the row vector of 1 * n used by fminunc
        x0 = zeros(1, n);
        % gradient descent
        % theta is a row vector of 1 * n
        
        [theta, ~, exitflag] = fminunc(@cost_function, x0, options);
        if (exitflag == 0)
            lambda = lambda * 2;
            continue
        end
        
        prediction = sigmod(theta, CV);
        %dlmwrite(sprintf('prediction_%d.csv', file_cnt), prediction, 'delimiter', '\n');
        file_cnt = file_cnt + 1;
        %cross validation
        [~, ~, ~, AUC] = perfcurve(y_cv, prediction, 1);
        display(sprintf('AUC = %d, lambda = %d', max(AUC, 1 - AUC), lambda));
        if max(AUC, 1 - AUC) > AUC_result
            AUC_result = max(AUC, 1 - AUC);
            lambda_result = lambda;
            theta_result = theta;
        end
        lambda = lambda * 2;
    end
    
    prediction = sigmod(theta_result, T);
	%calculate AUC and print ROC curve
	[X, Y, ~, AUC] = perfcurve(y_t, prediction, 1);
	AUC = max(AUC, 1 - AUC)
    lambda_result
	dlmwrite('hypothesis.csv', theta_result(1, 2 : n), 'delimiter', '\n');
    
    
	%generate test prediction
    test_set = dlmread('test1.csv');
	B = spconvert(test_set);
    B = full(B);
    [tm, tn] = size(B);
    B = [ones(tm, 1), B];
	prediction = sigmod(theta, B);
	dlmwrite('prediction.csv', prediction, 'delimiter', '\n');
end

% x is a row vector of 1 * n
% A is a matrix of m * n
function f = sigmod(x, A)
	f = 1 ./ (1 + exp(-x * A'));
end

%divide the training set to 60, 20, 20
%for cross validation
function [B, CV, T, y_a, y_cv, y_t] = divide(A, y)
    [tm, tn] = size(y);
    [m, n] = size(A);
    if m < tm
        A = [A; zeros(tm - m, n)];
    end
    [m, n] = size(A);
    m = floor(m * 0.2);
    t1 = floor(m * 0.6);
    t2 = floor(m * 0.2);
    t3 = m - t1 - t2;
    B = A(1: t1, 1 : n);
    CV = A(t1 + 1: t1 + t2, 1 : n);
    T = A(t1 + t2 + 1 : m, 1 : n);
    y_a = y(1, 1 : t1);
    y_cv = y(1,  t1 + 1: t1 + t2);
    y_t = y(1, t1 + t2 + 1 : m);
end
