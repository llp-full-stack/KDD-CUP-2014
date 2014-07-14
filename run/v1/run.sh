#!/bin/bash

echo picking and shuffling
python pick_and_shuffle.py

echo converting test set
ruby translate_test.rb

echo converting training set
echo a few steps to go...
ruby translate_train.rb

echo ok, run matlab 
matlab -nodisplay -nojvm < run_logis_reg.m
