# EtfB Phylogenetic Analysis

## Files and commands used to align EtfB homologs and produce a phylogenetic tree.

### Aligning EtfB homologs

EtfB homologs were identified from MAGs in the Intermediate Chain Elongators and Carbohydrate Chain Elongators functional groups using BLAST and known EtfB protein sequences from genomes. Homologs were selected as those with a percent identity >25% and a query length greater than 70%.

The `etfB_homologs_for_plylogenetic_tree.fasta` files contains the homologs and EtfB protein sequences used in this analysis.

To align the genome, `muscle` (v.3.8.31) was used:

`muscle -in etfB_homologs_for_phylogenetic_tree.fasta -out etfB_homologs_for_phylogenetic_tree_aligned.fasta`

### Making the phylogenic tree

RAxML-ng (v0.9.0) was used to parse the alignment file:

`raxml-ng --parse --msa etfB_homologs_for_phylogenetic_tree_aligned.fasta --model LG+G8+F --prefix T1`

And then this parsed file was used to construct the phylogenetic tree using RAxML-ng:

`raxml-ng --all --msa T1.raxml.rba --model LG+G8+F --prefix etfA_tree --bs-trees 500 --threads 7 --seed 2`

The resulting tree (`etfA_etfB_homologs_for_phylogenetic_tree.support`) was edited for publication in [TreeViewer](https://treeviewer.org "Flexible, modular software to visualise and manipulate phylogenetic trees") and Illustrator.