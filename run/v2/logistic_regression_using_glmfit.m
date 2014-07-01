function logistic_regression_using_glmfit ..., 
    (training_file, outcome_file, test_file, assessment_percentage)

    [training, training_outcome, test, assessment, assessment_outcome] = read_data(training_file, outcome_file, test_file, assessment_percentage);
    
    %training_cnt = size(training, 1);
    [B, fit_info] = lassoglm(training, training_outcome, 'binomial', ...,
                             'Alpha', 0.001, 'CV', 5, 'NumLambda', 20);
    
    chosen_lambda_index = fit_info.IndexMinDeviance;
    chosen_lambda = fit_info.Lambda(1, chosen_lambda_index);
    
    hypothesis = B(:, chosen_lambda_index);
    
    %assessment_cnt = size(assessment, 1);
    assessment_hat = glmval(hypothesis, assessment, 'logit', 'Constant', 'off');
    
    [~, ~, ~, AUC] = perfcurve(assessment_outcome, assessment_hat, 1);
    
    dlmwrite('lambda_all.csv', fit_info.Lambda);
    dlmwrite('hypothesis_all.csv', B, ','); % print hypothesis
    
    fprintf('lambda = %f, deviance = %f\n', chosen_lambda, fit_info.Deviance(1, chosen_lambda_index));
    fprintf('AUC on assessment set = %f\n', AUC);
    
    %test_cnt = size(assessment, 1);
    prediction = glmval(hypothesis, test, 'logit', 'Constant', 'off');
    

    dlmwrite('hypothesis.csv', hypothesis);
    dlmwrite('prediction.csv', prediction);
    
    function [training, training_outcome, test, assessment, assessment_outcome] = read_data(training_file, outcome_file, test_file, assessment_percentage)
        sparse_mat = dlmread(training_file);    % the features
        mat = full(spconvert(sparse_mat));
        outcome = dlmread(outcome_file);    % the labels
        [N, ~] = size(mat);
        training_cnt = floor((1 - assessment_percentage) * N);
        
        training = mat(1 : training_cnt, :);
        training_outcome = outcome(1 : training_cnt);
        assessment = mat(training_cnt + 1 : N, :);
        assessment_outcome = outcome(training_cnt + 1 : N);
        
        sparse_mat = dlmread(test_file);
        test = full(spconvert(sparse_mat));
    end

%     function [training, training_outcome, CV, CV_outcome, verification, verification_outcome] ..., 
%             = read_training(training_file, outcome_file, training_percentage, CV_percentage)
%         sparse_mat = dlmread(training_file);    % the features
%         mat = full(spconvert(sparse_mat));
%         [N, ~] = size(mat);    % size of training set in total
%         outcome = dlmread(outcome_file);    % the labels
%         
%         training_cnt = floor(training_percentage * N);  % training part size
%         CV_cnt = floor(CV_percentage * N);     % CV part size
%         
%         training = mat(1:training_cnt, :);
%         training_outcome = outcome(1:training_cnt, :);
%         
%         CV = mat(training_cnt + 1 : training_cnt + CV_cnt, :);
%         CV_outcome = outcome(training_cnt + 1 : training_cnt + CV_cnt, :);
%         
%         verification = mat(training_cnt + CV_cnt + 1 : N, :);
%         verification_outcome = outcome(trainining_cnt + CV_cnt + 1 : N, :);
%         
%         
end