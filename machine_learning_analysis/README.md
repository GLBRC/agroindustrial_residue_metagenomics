# Machine Learning Analysis

This directory houses scripts and files used to perform machine learning analysis on the MAGs.

## Run the machine learning algorithm with `autoML.py`
The `autoML.py` script contains the required commands for training the training set, providing the best model, and then running the test data set with this model to produce the classification predictions.

Must be run in the same directory as the example files (copy the files into a new directory)

Using [this site](https://www.freecodecamp.org/news/classification-with-python-automl/) as a guide.

Requires pandas, numpy, and AutoML python modules

`python auotML.py`

## PacBio Samples
The input and output files for the MAGs assembled from PacBio sequence data:

 - x_train.txt = training set data
 - y_train.txt = training set classifications
 - x_test.txt = test data for PacBio MAGs
 - y_predicted_PacBio.txt = predicted classification for the PacBio MAGs

## Illumina Samples
The input and output files for the MAGs assembled from Illumina sequence data:

 - x_train.txt = training set data
 - y_train.txt = training set classifications
 - x_test.txt = test data for Illumina MAGs
 - y_predicted_illumina.txt = predicted classification for the Illumina MAGs
