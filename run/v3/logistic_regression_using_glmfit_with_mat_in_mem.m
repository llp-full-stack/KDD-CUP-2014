function logistic_regression_using_glmfit_with_mat_in_mem ..., 
    (test, training, training_outcome, assessment, assessment_outcome)

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
end