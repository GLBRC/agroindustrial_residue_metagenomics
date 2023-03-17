#!/usr/bin/env python
# coding: utf-8

# In[8]:


###################
# Annotation_informed_functional_assignments.py
# Copyright 2023, Abel Ingle, Kevin Myers, and Daniel Noguera
# Revised: March 15, 2023
###################

"""
Description
-----------
Annotation_informed_functional_assignments.py may be used to search GenBank files generated 
by NCBI's PGAP [1] for set of Enzyme Comission (EC) numbers associated with enzymes 
commonly identified in fermentative metabolisms of anaerobic microbiomes. 
Additionally, the script generates comparisons between BLAST based and NCBI annotation informed analyses.

Annotation_informed_functional_assignments.py performs multiple tasks: 
    - queries GenBank files for select EC numbers
    - compares BLAST based and annotation informed functional assignments of select 
      metabolic reactions
    - generates Venn diagrams of the two sets (BLAST based and annotation informed)
    - predicting if full, select fermentative pathways are either encoded or annotated for within a genome
    
The results will be three text files and two directories:
    1. 'NCBI_annotation_based_functional_assignment.txt': a presence / absence matrix (text file)
       of 0's and 1's wherein, for each genome, a cell with '0' indicates a predicted absence of 
       protein encoding region(s) associated with a metabolic reaction's enzyme, and a cell with '1'
       indicates a presence of such.
       
    2. 'BLAST_EC_set_operations.txt': a text file comparing BLAST based and annotation informed 
       functional assignments
       
    3. 'genomic_potential_reactions.txt': a text file of functional assignments informed by
       by both BLAST based and annotation informed analyses
       
    4. a directory of Venn diagrams graphically comparing BLAST based and annotation informed 
       functional assignments
       
    5. a set of text files indicating if a genome possesses the encoding regions for enzymes involved in 
       substrate-specific fermentative pathway ('1') or not ('0'), and what enzymes are missing  
       
    6. a set of text files indicating if a genome possesses the encoding regions for enzymes involved in
       substrate-specific fermentative pathways ('1') or not ('0')


Note that Blast_and_assign_function.py must be successfully ran prior to use 
of Annotation_informed_functional_assignments.py. However, this script can be easily manipulated 
to only perform an NCBI annotation, EC number based functional assignment with no comparison.


Notes
-----

    inputs : user-set directory of GenBank files obtained from NCBI and generated by PGAP [1]
             set text file associating metabolic reactions with EC numbers, 'metabolic_reactions.txt'
             text file generated by Blast_and_assign_function.py, 'BLAST_based_functional_assignment.txt'
             
    
    outputs: set of files from EC based functional assignments and comparisons (see Description);
             a directory of Venn diagrams
    
    Directories created:
        - Venn_diagrams                    - stores .pdf files of Venn diagrams for each genome,
                                             in 'output' directory
        - BLAST_annotation_fermentations   - information on the genomic potentials of fermentative metabolic functions,
                                             in 'output' and based on BLAST and NCBI annotation EC numbers
    
    dependencies : 
        - python 3
        - Python modules pathlib, subprocess, pandas, Bio, matplotlib_venn, matplotlib
        
    usage [standard]:
        python3 Annotation_informed_functional_assignments.py
        
References : [1] https://www.ncbi.nlm.nih.gov/genome/annotation_prok/
"""

# Import packages

import pandas as pd
from pathlib import Path
from Bio import SeqIO
import re
import subprocess
from subprocess import run, Popen, PIPE
import pandas as pd
from matplotlib_venn import venn2, venn2_circles
from matplotlib import pyplot as plt

# The paths of these directories should be consistent with your filenaming scheme

reactions_table=pd.read_table("codefiles/metabolic_reactions.txt", encoding='latin-1').fillna('')

# Create a dictionary of EC numbers associated with reach metabolic reaction

ecnumbers={}
for row, index in reactions_table.iterrows():
    if index["Enzyme comission number"]=='':
        pass
    else:
        ecnumbers.update({index["Reaction ID"]:index["Enzyme comission number"]})

# Create a dataframe to be populated with 0's and 1's associated with each reaction-genome combination

ec=pd.DataFrame(ecnumbers.keys(), index=ecnumbers.keys())
ec=ec.rename(columns=({0:"BiGG Models Name"}))

# Introduce file paths of each NCBI annotation

NCBI_annotation_directory='codefiles/NCBI_annotations/'
NCBI_annotation_files=Path(NCBI_annotation_directory).glob('*.gbff')

for ncbi_anno in NCBI_annotation_files:
    genome = ncbi_anno.stem
    
    # Now, add columns with genomes as headers and '0' values
    
    if genome not in ec.columns:
        ec.insert(len(ec.columns),column=genome,value=0)
    
    # Compile all EC numbers in GenBank files
    
    gbff_annos = []
    for record in SeqIO.parse(ncbi_anno, 'genbank'):
        for f in record.features:
            if f.type == "CDS":
                if "EC_number" in f.qualifiers:
                    for number in f.qualifiers["EC_number"]:
                        gbff_annos.append(number)
    
    # Eliminate repeated EC numbers
    
    final_list_ec_nos_per_genome=set(gbff_annos)

    
    # Check if each metabolic reactions associated EC number(s) is in the GenBank annotation
    
    for key, value in ecnumbers.items():
        if "or" in value:
            ecn=value.split(" or ")
            enzyme_comission_threshold = any(e in final_list_ec_nos_per_genome for e in ecn)
            
        elif "and" in value:
            ecn=value.split(" and ")
            enzyme_comission_threshold = all(e in final_list_ec_nos_per_genome for e in ecn)
        
        elif value in final_list_ec_nos_per_genome:
            enzyme_comission_threshold = True
            
        else:
            enzyme_comission_threshold = False
                
        # If associated EC number(s) is in GenBank annotation, assign '1' value
        
        if enzyme_comission_threshold is True:
            ec.at[key,genome]=1
            
            
        else:
            pass
        
id_to_reaction_dic={}
for row, index in reactions_table.iterrows():
    id_to_reaction_dic.update({index["Reaction ID"]:index["Reaction Name"]})
    
for key in ecnumbers.keys():
    ec.at[key,"BiGG Models Name"]=id_to_reaction_dic[key]

ec.set_index("BiGG Models Name",drop=False)
    
ec.to_csv("output/NCBI_annotation_based_functional_assignment.txt",index=None,sep="\t",mode="w")

print("Done with NCBI annotation informed metabolic assignments.")


### Code below line may be deleted if you do not want to compare results 
### with BLAST based assignments. Doing so forgoes the prerequisite use
### of Blast_and_assign_function.py; matplotlib_venn, matplotlib, and subprocess modules
### -------------------------------------------------------------------------------------------------

# Set paths to genomic files

cMAG_directory= 'refgenomes'
cMAG_files=Path(cMAG_directory).glob('*.fna')

# Reestablish DataFrame such that only reactions with associated EC numbers are involved

ec_wo_ind=pd.read_csv("output/NCBI_annotation_based_functional_assignment.txt",sep="\t")
ec=ec_wo_ind.set_index("BiGG Models Name",drop=False)

mf_wo_ind=pd.read_csv("output/BLAST_based_functional_assignment.txt",sep="\t")
mf=mf_wo_ind.set_index("BiGG Models Name",drop=False)
final=mf

reactions_table=pd.read_table("codefiles/metabolic_reactions_ICEC.txt", encoding='latin-1').fillna('')

ecnumbers={}
for row, ind in reactions_table.iterrows():
    if ind["Enzyme comission number"]=='':
        pass
    else:
        ecnumbers.update({ind["Reaction ID"]:ind["Enzyme comission number"]})

# Make a directory to store Venn diagrams
        
mk_Venndiagram_directory='mkdir output/Venn_diagrams'

subprocess.run([mk_Venndiagram_directory],shell=True)

        
for cmag in cMAG_files:
    
    # Store the set operations
    
    #Ab = Contained in group A, but not B
    Ab=0

    #aB = Contained in group B, but not A
    aB=0

    #AB = Contained in both group A and B
    AB=0

    #ab = Contained in neither group A nor B
    ab=0

    # Make Venn diagrams
    
    for index in ec.index:
        if ec.at[index,cmag.stem] == 1 and mf.at[index,cmag.stem] == 1:
            AB=AB+1
            ec.at[index,cmag.stem]="AB"
        elif ec.at[index,cmag.stem] == 1 and mf.at[index,cmag.stem] != 1:
            Ab=Ab+1
            ec.at[index,cmag.stem]="A"
            final.at[index,cmag.stem]=1
        elif ec.at[index,cmag.stem] != 1 and mf.at[index,cmag.stem] == 1:
            aB=aB+1
            ec.at[index,cmag.stem]="B"
        else:
            ec.at[index,cmag.stem]=""
    
    # Label figures
    number_of_absent_reactions=str(ab)
    venn2(subsets = (Ab, aB, AB), set_labels = ('NCBI annotation informed', 'BLAST based'),
          set_colors=('red','blue'),
          alpha = 0.5);
    venn2_circles(subsets = (Ab, aB, AB))
    plt.title(cmag.stem+" ("+number_of_absent_reactions+" reactions absent)")
    plt.savefig('output/Venn_diagrams/{0}.png'.format(cmag.stem), facecolor="white", format="png")
    plt.close()

ec.to_csv("output/BLAST_EC_set_operations.txt",index=None,sep="\t",mode="w")
header = 'echo "A: Annotation informed \nB: BLAST based \nAB: Both \nBlank: neither\n" | cat - output/BLAST_EC_set_operations.txt > temp && mv temp output/BLAST_EC_set_operations.txt'
header_process = subprocess.run(header,
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)

final.to_csv("output/genomic_potential_reactions.txt", index=None,sep="\t",mode="w")

print("Done comparing BLAST based and NCBI annotation informed analyses.")

# Rename DataFrame 

gpr=final

# Make directory to store fermentative pathway assignments

subprocess.call(["mkdir", "output/BLAST_annotation_fermentations"])

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
                    
                    # Append list of reactions missing for every substrate-specific pathway
                    
                    if question is False:
                        missing_reactions.append(sole_e_donor_pathways.at[row,pw])
                        
            fermentative_lifestyles.at[pw,cmag.stem+"_missing_reactions"]=missing_reactions
            
            # If all biochemical reactions required for the pathway have at least one enzyme assigned 
            # a '1' in the functional assignments, then the genome receives a '1' in the pathways DataFrame.
            
            if all(truths is True for truths in truth):
                fermentative_lifestyles.at[pw,cmag.stem]=1
                fermentative_lifestyles2.at[pw,cmag.stem]=1
                print(cmag.stem,"can perform",pw,"fermentation using",key,"as an electron donor.")
               
    fermentative_lifestyles.to_csv("output/BLAST_annotation_fermentations/{}_fermentations_missing_reactions.txt".format(key), index=None,sep="\t",mode="w")
    fermentative_lifestyles3=fermentative_lifestyles2.transpose()
    fermentative_lifestyles3.to_csv("output/BLAST_annotation_fermentations/{}_fermentations.txt".format(key),sep="\t",header=None,mode="w")
print("Done predicting substrate-specific fermentative pathways.")
