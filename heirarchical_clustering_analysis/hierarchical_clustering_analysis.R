#heirarchical_clustering_analysis
#2023-03-22

library(tidyverse)
library(gplots)
library(viridis)

#set working directory to include the "percentage_pathways.txt" file

percKW <- read.table(file = "percentage_pathways.txt", sep = "\t", header = TRUE, row.names = "MAG")
percKW.matrix <- as.matrix(percKW)
setEPS()
postscript("Percentage_Pathway_Clustering_Analysis.eps")
heatmap.2(percKW.matrix, density.info = "none", dendrogram = "row", trace = "none",
          breaks = c(0,0.25,0.5,0.75,1),
          col = (c("white","darkgoldenrod1", "coral1", "sienna3")),
          sepwidth = c(0.01, 0.01), Rowv=T, Colv=FALSE, margins = c(10,10), cexRow = 0.1, cexCol = 0.1)
dev.off()
