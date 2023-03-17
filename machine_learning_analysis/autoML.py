#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Simple machine learning alrogithm for using Abel's BLAST data results

Training set = known lactic acid and chain elongator genomes
Testing set = MAGs

Will compare all possible ML algorithms and show best one. Then write results

Need to clean up but works.

Followed this:  https://www.freecodecamp.org/news/classification-with-python-automl/

Created on Fri Jan  6 10:32:37 2023

@author: kevinmyers
"""
import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from supervised.automl import AutoML

y = pd.read_table("y_train.txt", header = None)
y_train = pd.Series(y[0], name = "target")
X_train = pd.read_table('X_train.txt')
X_test = pd.read_table('X_test.txt', index_col=0, header=0)

automl = AutoML(algorithms=["Decision Tree", "Linear", "Random Forest", "Xgboost", "Neural Network", "Nearest Neighbors", "Extra Trees", "CatBoost", "LightGBM", "Baseline"],
                total_time_limit=10*60)
automl.fit(X_train, y_train)

y_predicted = automl.predict(X_test)

y_predicted.tofile("y_predicted.txt", sep = "\t")