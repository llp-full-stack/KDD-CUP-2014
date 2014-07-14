KDD-CUP-2014
============

KDD-CUP-2014 Predicting Excitement at DonorsChoose.org

Team Segmentation Fault

Team Member:
Chen Hao, Jin Wengong, Peng Yanqing, Zhao Zhuoyue

###Data processing:

* data_processing/donation.rb (by Chen Hao): pick and convert features from donation.csv
* data_processing/outcomes.rb (by Peng Yanqing): pick and convert labels from outcomes.csv
* data_processing/essay_length.rb (by Chen Hao): calculate essay length from essays.csv
* data_processing/projects.py (by Zhao Zhuoyue): pick and convert features from projects.csv
* data_processing/resources.py (by Jin Wengong): pick and convert features from resources.csv (missing)

The above programs create separate files. They can be converted to a SVDFeature format sparse matrix using process.py (by Zhao Zhuoyue). Due to SVDFeature's poor performance, we switched to MATLAB. The SVDFeature format sparse matrix has to be further converted to MATLAB format sparse matrix, which will be discussed in next part.

The following programs deal with specific features:

* data_processing/separate_positive_and_negative.py : separate positive and negative data
* data_processing/stat_outcomes_by_time_posted.py : calculate the number of positive samples by the time posted
* data_processing/filter_project_after_time_posted.py : output the ids of project after given time posted
* data_processing/filter_id_by_file.py : create a mask file according to the id file created by filter_project_after_time_posted and ids missing from new_resources.csv
* data_processing/apply_mask_to_negative.py : apply the mask to the negative data
* data_processing/process_new_resources.py : change the representation of some features extracted from resources.csv
* data_processing/stat_exciting_rate.py : calculate the exciting rate of some category features as new features
* data_processing/feature_classifier.rb : separate the entire SVDFeature format sparse matrix to files each of which contains only one feature

###Logistic Regression Impl.

We have three versions of logistic regeression implementation. v1 is a hand-written logistic regression using the fminunc function. v2 and v3 uses the MATLAB Generalized Linear Model Fitting (glmfit). v3 preloads the data matrix into the memory so that it can support multiple runs without reading again from files.

translate.rb is written by Peng Yanqing. submission_gen.rb is written by Chen Hao. v1 logistic_regression.m is written by Jin Wengong. v2 and v3 logistic_regression_using_glmfit.m and logistic_regression_using_glmfit_in_mem.m is written by Zhao Zhuoyue.

* v1 : hand-written logistic regression using fminunc. It, however performed poorly due to using AUC as standard to evaluate the effect of regularization. Need to run pick_and_shuffle.py to pick data from training_positive.csv and traning_negative.csv. Then run translate_train.rb and translate_test.rb first to convert traning_partial.csv and test.csv to MATLAB sparse matrix. The features used picked by the translator can be configured using conf file. (Refer to conf_xxxx files) At last, use MATLAB to run logistic_regression.m. The generated prediction combined with test_report.txt (project ids) can generate submission.csv in required form.

* v2 : uses the MATLAB glmfit function lassoglm, which is configured to perform logistic regression and apply 5-fold cross-validation on 20 regularization factors. The usage of other tools are the same as v1. Features after 525 are not available to v1 and v2.

* v3 : preloads the matrix to the memory. One benefit is that multiple runs with tweaks can be performed without reading from file for multiple times. (file operation are very slow) The usage of v3 also changed. First configure the features as in matlab_config. Then run generate_matlab_load_file.py to generate load_data.m. At last run run_logis_reg_glmfit_with_mat_in_mem.m. to run the entire regression program. To re-run the logistic regression after the first run, invoke logistic_regression_using_glmfit_with_mat_in_mem.m as in run_....m. Finally run submission_gen.rb to generate file in required form. v3 needs the data in training_negative, training_positive and test folders and test_report.txt.


###Micellaneous

Programs in misc folder are undocumented and uncategorized code.