#!/usr/bin/env python
# coding: utf-8

# In[37]:


###################
# Blast_and_assign_function.py
# Copyright 2023, Abel Ingle, Kevin Myers, and Daniel Noguera
# Revised: March 14, 2023
###################

"""
Description
-----------
Blast_and_assign_function.py may be used to quickly perform Basic Local Alignment Search Tool (BLAST) [1]
using a set of query protein sequences associated with enzymes commonly identified in fermentative metabolisms of
anaerobic microbiomes. By using this script, the user may identify sequences in their own genome set that are
highly similar to query proteins, and predict metabolic functions based on those sequences.

Blast_and_assign_function.py performs multiple tasks: 
    - performing BLAST (tBLASTn mode) to align query protein sequences with subject genome sequences using
      BLAST, and generating the subject sequences and other information for each high-scoring sequence pair. 
    - tallying the number of hits per query protein per genome
    - predicting the presence or absence of enzyme encoding regions within a genome
    - predicting if full, select fermentative pathways are encoded for within a genome
    
The results will be a directory 'output' with four text files and one directory:
    1. 'tBLASTn_summary.txt': a text file with all BLAST hits (all query proteins against each genome)
    
    2. 'filtered_tBLASTn_summary.txt': a text file with all BLAST hits that met parameter cutoffs
       ("pident" > 25% and "qcovhsp" > 70%)
    
    3. 'protein_encoding_copy_assignments.txt': a text file with tallies of all query protein hits
        that passed the filter step per genome
    
    4. 'BLAST_based_functional_assignment.txt': a presence / absence matrix of 0's and 1's wherein,
       for each genome, a cell with '0' indicates a predicted absence of protein encoding region(s)
       associated with a metabolic reaction's enzyme, and a cell with '1' indicates a presence of such.
       
    5. a set of text files indicating if a genome possesses the encoding regions for enzymes involved in 
       substrate-specific fermentative pathway ('1') or not ('0'), and what enzymes are missing  
       
    6. a set of text files indicating if a genome possesses the encoding regions for enzymes involved in
       substrate-specific fermentative pathways ('1') or not ('0')

Notes
-----

    inputs : user-set directory of genomic nucleotide sequences named 'refgenomes';
             set directory of protein sequences, 'queryprotein';
             set of files relating information about proteins, metabolic reactions, and fermentative pathways, in 'codefiles' directory
             
    
    outputs: a directory that stores BLAST databases, 'databases';
             a directory that stores all results (see Description)
    
    Directories created:
        - databases               - BLAST nucleotide type database files (.nhr, .nin, and .nsq) per genome
        - output                  - directory storing all results
        - BLAST_fermentations     - information on the genomic potentials of fermentative metabolic functions,
                                    in 'output' and based on BLAST
        

    
    dependencies : 
        - python 3
        - Python modules pathlib, subprocess, pandas, numpy
        
    usage [standard]:
        python3 Blast_and_assign_function.py
        
References : [1] https://doi.org/10.1186/1471-2105-10-421
"""

# Import packages

from pathlib import Path
import subprocess
from subprocess import run, Popen, PIPE
import pandas as pd
import numpy as np


# The TSV formatted filename downloaded from UniProtKB is to be copied and pasted below

uniprot_table=pd.read_table("codefiles/uniprot-compressed_true_download_true_fields_accession_2Cid_2Cprotei-2023.02.20-18.16.06.19.tsv")
uniprot_table.index=uniprot_table["Entry"]
protein_directory = 'queryproteins'
ids=pd.read_table("codefiles/MAG_names_accessions_ids.txt")
ids=ids.set_index("Strain",drop=False)

# The glob module used below relies on the .FASTA file extension to be consistent for all protein sequences in uniprot_fastas_directory    

cMAG_directory= 'refgenomes'
cMAG_files = Path(cMAG_directory).glob('*.fna')

# Make a BLAST nucleotide type database for every genome sequence in 'refgenomes' directory, externally

for cmag in cMAG_files:
    makeblastdb = 'makeblastdb -in {0} -dbtype nucl -out databases/{1}'.format(cmag,cmag.stem)
    
    DB_process = subprocess.run(makeblastdb,
                                  shell=True,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  check=True,
                               text=True)


# Make a text file to store all BLAST hits, 'tBLASTn_summary.txt', and read it as a DataFrame

protein_directory = 'queryproteins'
protein_files = Path(protein_directory).glob('*.faa')

BLAST_summary='mkdir output; echo "Sequence_ID\tSequence_start\tSequence_end\tPercent_identity\tLength\tEvalue\tQuery_coverage\tSequence\tGenome\tUniProt_ID\tUniProt_name" > output/tBLASTn_summary.txt'
subprocess.run([BLAST_summary],shell=True)
tBLASTn_df=pd.read_table('output/tBLASTn_summary.txt')

# Reestablish file paths after every subprocess is ran

cMAG_directory= 'refgenomes'
cMAG_files = Path(cMAG_directory).glob('*.fna')
protein_directory = 'queryproteins'
protein_files = Path(protein_directory).glob('*.faa')

# For-loop running BLAST in tBLASTn mode for every query protein for every genome

starting_index=0

for cmag in cMAG_files:
    protein_files = Path(protein_directory).glob('*.faa')
    
    for prot in protein_files:
        tblastncmd = 'tblastn -query {0} -db databases/{1} -outfmt "6 sseqid sstart send pident length evalue qcovhsp sseq" -evalue 1e-10 >> output/tBLASTn_summary.txt'.format(prot,cmag.stem,cmag.stem,prot.stem)
        tblasn_process = subprocess.run(tblastncmd,
                                          shell=True,
                                          stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                          text=True)
        tBLASTn_df=pd.read_table('output/tBLASTn_summary.txt')
        
        # Populate DataFrame and text file of BLAST hits
        
        if tBLASTn_df.empty == True:
            ending_index=0
        else:
            ending_index=tBLASTn_df.index.stop
        prot_name=uniprot_table.at[prot.stem,"Protein names"]
        for cell in range(starting_index, ending_index):
            tBLASTn_df.at[cell,"Genome"]=cmag.stem
            tBLASTn_df.at[cell,"UniProt_ID"]=prot.stem
            tBLASTn_df.at[cell,"UniProt_name"]=prot_name
            tBLASTn_df.to_csv("output/tBLASTn_summary.txt",index=None,sep="\t",mode="w")
        starting_index=ending_index

# Truncate the BLAST hits summary to only hits that satisfy cutoff parameters and generate text file output

filtered_data = tBLASTn_df.loc[(tBLASTn_df["Query_coverage"] > 70) & (tBLASTn_df["Percent_identity"] > 25)]
filtered_data.to_csv("output/filtered_tBLASTn_summary.txt",index=None,sep="\t",mode="w")

print("Done BLASTing.")

# Reestablish file paths after every subprocess is ran

protein_directory = 'queryproteins'

# Make DataFrame indexed with query proteins to tally number of filtered BLAST hits per protein per genome

prots=list()
protein_files = Path(protein_directory).glob('*.faa')
for prot in protein_files:
    prots.append(prot.stem)
gene_copy_assignment={'UniProt ID': prots}
gca=pd.DataFrame(gene_copy_assignment, index=prots)

# Parse filtered BLAST hits DataFrame, 'filtered_tBLASTn_summary.txt' 

for index, row in filtered_data.iterrows():
    if row['Genome'] not in gca.columns:
        gca.insert(len(gca.columns),column=row['Genome'],value=0)
    else:
        pass
    
    # Tally the number of hits per protein per genome in DataFrame and generate text file output
    
    gca.at[row['UniProt_ID'],row['Genome']]=gca.at[row['UniProt_ID'],row['Genome']]+1

gca.to_csv("output/protein_encoding_copy_assignments.txt",index=None,sep="\t",mode="w")

# Read in text file with summary of proteins associated with each metabolic reaction as DataFrame

reactions_table=pd.read_table("codefiles/metabolic_reactions.txt", encoding='ISO-8859-1').fillna('')

unique_reactions=reactions_table["Reaction ID"].unique()
reactions=list(unique_reactions)

reactions_and_uniprotids={}
for reaction in reactions:
    reactions_and_uniprotids.update({reaction:[]})

# Make a dictionary with metabolic reactions as keys and proteins as values

for row, index in reactions_table.iterrows():
    if index["Reaction ID"] in reactions_and_uniprotids.keys():
        reactions_and_uniprotids[index["Reaction ID"]].append(index["UniProt ID"])
    else:
        pass

"""
Index a DataFrame with metabolic reactions to make a presence '1' / absence '0' matrix of protein encoding
region(s) associated with each metabolic reactions to each genome
"""

metabolic_function={"BiGG Models Name": reactions}
mf=pd.DataFrame(metabolic_function, index=reactions)
for column in gca.columns[1:]:
    if column not in mf.columns:
        mf.insert(len(mf.columns),column=column,value=0)
        
        # For-loop through DataFrame for each metabolic reaction
        
        for reaction in reactions:
            gene_copy_numbers=list()
            for uniprotid in reactions_and_uniprotids[reaction]:
                gene_copy_number=gca.at[uniprotid,column]
                gene_copy_numbers.append(gene_copy_number)
                
            # Conditional statement such that all proteins associated with each metabolic reaction must 
            # have a BLAST hit in order for the reaction-genome cell to receive a '1'
            
            reaction_proceeds = all(gcn > 0 for gcn in gene_copy_numbers)
            if reaction_proceeds is True:
                mf.at[reaction,column]=1
            else:
                pass
        
    else:
        pass

# Reindexing for DataFrame reading

id_to_reaction_dic={}
for row, index in reactions_table.iterrows():
    id_to_reaction_dic.update({index["Reaction ID"]:index["Reaction Name"]})
    
for key in id_to_reaction_dic.keys():
    mf.at[key,"BiGG Models Name"]=id_to_reaction_dic[key]
    
# Generate text file for presence '1' / absence '0' matrix

mf.to_csv("output/BLAST_based_functional_assignment.txt",index=None,sep="\t",mode="w")

print("Done with BLAST based metabolic assignments.")

gpr=mf.set_index("BiGG Models Name",drop=False)

# Make directory to store fermentative pathway assignments

subprocess.call(["mkdir", "output/BLAST_fermentations"])

# Excel file that summarizes various fermentation pathways of various substrates is read as DataFrame

fermentative_lifestyle_reqs=pd.read_excel("codefiles/fermentation_requirements.xlsx",sheet_name=None)

# For every substrate of interest, make a DataFrame of substrate-specific pathways, 
# and their respective biochemical reactions involved

for key in fermentative_lifestyle_reqs.keys():
    sole_e_donor_pathways=pd.DataFrame(fermentative_lifestyle_reqs[key].fillna(''))
    pathways=list(sole_e_donor_pathways.columns)
    fermentations={key+"_fermentation_pathways": pathways}
    
    # A DataFrame indexed with substrate-specific pathways
    # that summarizes the presence / absence of each genome's pathway-specific protein encoding regions
    
    fermentative_lifestyles=pd.DataFrame(fermentations, index=pathways)
    fermentative_lifestyles2=pd.DataFrame(fermentations, index=pathways)
    
    # For every pathway queried per substrate
    
    for pathway in sole_e_donor_pathways.columns:
        
        # For every step of every pathway, make reactions possible into a list
        
        for row, index in sole_e_donor_pathways.iterrows():
            """
            For some metabolic reactions within a pathway, 
            sufficient biochemistry can proceed with varying enzymes or complexes;
            hence, an "or" condition is used.
            """
            
            if sole_e_donor_pathways.at[row,pathway] == "":
                pass
            
            else:
                split_cell=sole_e_donor_pathways.at[row,pathway].split(" or ")
                sole_e_donor_pathways.at[row,pathway]=split_cell
                
    # Now, add columns with genomes as headers
    
    cMAG_directory= 'refgenomes'
    cMAG_files=Path(cMAG_directory).glob('*.fna')
    
    for cmag in cMAG_files:
        
        for pw in pathways:
            
            if cmag.stem not in fermentative_lifestyles.columns:
                
                fermentative_lifestyles.insert(len(fermentative_lifestyles.columns),column=cmag.stem,value=0)
                fermentative_lifestyles2.insert(len(fermentative_lifestyles2.columns),column=cmag.stem,value=0)
                fermentative_lifestyles.insert(len(fermentative_lifestyles.columns),column=cmag.stem+"_missing_reactions",value="")
                
            truth=list()
            
            missing_reactions=list()
            
            """
            Parse DataFrame, and check if the BLAST based functional assignment indicated a 1 or 0
            for every biochemical reaction for every genome. If 0's are involved, add biochemical 
            reaction to list of missing reactions.
            """
            
            for row,index in sole_e_donor_pathways.iterrows():
                if sole_e_donor_pathways.at[row,pw]=="":
                    pass
                else:
                    question=any(gpr.at[rxn,cmag.stem] == 1 for rxn in sole_e_donor_pathways.at[row,pw])
                    truth.append(question)
                    
                    if question is False:
                        missing_reactions.append(sole_e_donor_pathways.at[row,pw])
                        
            fermentative_lifestyles.at[pw,cmag.stem+"_missing_reactions"]=missing_reactions
            
            # If all biochemical reactions required for the pathway have at least one enzyme assigned 
            # a '1' in the functional assignments, then the genome receives a '1' in the pathways DataFrame.
            
            if all(truths is True for truths in truth):
                fermentative_lifestyles.at[pw,cmag.stem]=1
                fermentative_lifestyles2.at[pw,cmag.stem]=1
                print(cmag.stem," can perform ",pw," using ",key," as an electron donor.")
                
    fermentative_lifestyles.to_csv("output/BLAST_fermentations/{}_fermentations_missing_reactions.txt".format(key), index=None,sep="\t",mode="w")
    fermentative_lifestyles3=fermentative_lifestyles2.transpose()
    fermentative_lifestyles3.to_csv("output/BLAST_fermentations/{}_fermentations.txt".format(key),sep="\t",header=None,mode="w")
print("Done predicting substrate-specific fermentative pathways.")

