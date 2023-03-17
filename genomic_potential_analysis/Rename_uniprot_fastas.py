#!/usr/bin/env python
# coding: utf-8

# In[1]:


###################
# Rename_uniprot_fastas.py
# Copyright 2023, Abel Ingle, Kevin Myers, and Daniel Noguera
# Revised: March 14, 2023
###################

""""
Description
-----------
Rename_uniprot_fastas.py renames protein sequence files downloaded 
from UniProt as the UniProt ID associated with each sequence.

This script relies on UniProt's formatting of FASTA files headers [1].

Notes
-----

    inputs : directory of individual protein sequences in 'codefiles/' directory
    
    outputs : 'queryproteins' directory with renamed protein sequence files with .faa file extensions
    
    dependencies : 
        - python 3
        - Python modules pathlib, subprocess
        
    usage [standard]:
        Rename_uniprot_fastas.py
        
References : [1] https://www.uniprot.org/help/fasta-headers

"""


# Import packages

from pathlib import Path
import subprocess
from subprocess import run, Popen, PIPE

# The paths of these directories should be consistent with your filenaming scheme

uniprot_fastas_directory = 'codefiles/uniprot_fastas_split_files'
protein_directory = 'queryproteins'

# Make a directory 'queryproteins' to store renamed FASTA files

subprocess.call(["mkdir", protein_directory])

# The glob module used below relies on the .FASTA file extension to be consistent for all protein sequences in uniprot_fastas_directory    

uniprot_fastas = Path(uniprot_fastas_directory).glob('*.fasta')

for uniprot_fasta in uniprot_fastas:
    with open(uniprot_fasta, 'r') as u:
        line = (u.readlines(1))
        split_line=line[0].split("|")
        uniprot_id=split_line[1]
        rename_fasta_files="cp {0} {1}/{2}.faa".format(uniprot_fasta,protein_directory,uniprot_id)
        renaming_process = subprocess.run(rename_fasta_files,
                                  shell=True,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  check=True,
                                          text=True)

