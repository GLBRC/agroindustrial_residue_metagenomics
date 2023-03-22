# Agroindustrial Residue Metagenomics Scripts and Information


## Overview

This repository contains all scripts and example files referenced in _Comparison of metagenomes from fermentation of various agroindustrial residues suggests a common model of community organization_ manuscript (reference to come)

The different scripts are contained within different directories. Each directory has its own README to explain the files within.

## genomic_potential_analysis
This directory generates information about the fermentative genomic potentials of user-provided organisms. It infers the presence / absence of proteins and enzymes identified in fermentative metabolism of self-assembled anaerobic microbiomes fed agroindustrial residues. Outputs include Boolean matrices wherein 1's and 0's indicate the presences and absences, respectively, of coding regions for proteins and enzymes for every genome queried; comparisons of BLAST based and NCBI annotation informed analyses; and all supporting information.

## machine_learning_analysis
This directory contains the script and files used to train and run the machine learning classification algorithm to classify the MAGs.

## nmds_plot
This directory contains the script and file used to generate the Non-metric MultiDimensional Scaling (NMDS) plot used in the manuscript. Note that the figure was edited in Illustrator for publication.

## hierachical_clustering_analysis
This directory contains the script and file used to perform the hierarchical clustering analysis used in the manuscript. Note that the figure was edited in Illustrator for publication.

## Contributors
Kevin Myers, Abel Ingle, Daniel Noguera - all at University of Wisconsin-Madison

## Contact
Please reach out to Kevin Myers at kmyers2@wisc.edu
