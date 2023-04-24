#plotting NMDS plots for metagenomic data

library(ggplot2)
library(dplyr)
library(cowplot)
library(ggthemes)
library(RColorBrewer)
library(tidyverse)
library(forcats)
library(vegan)

Sys.setenv("R_REMOTES_NO_ERRORS_FROM_WARNINGS"=TRUE)
library(devtools)
install_github("pmartinezarbizu/pairwiseAdonis/pairwiseAdonis")
library(pairwiseAdonis)

#setwd("./example_files")
setwd("~/Desktop/nmds_files/")

data <- read.table(file = "rel_abund_allMAGS.txt", header = TRUE, sep = "\t")
data_melt <- reshape::melt(data, id.vars=c("Rel_Abundance"))
write.table(data_melt, file = "rel_abundance_allMAGS_long_from_R.txt", sep = "\t")

#edit file manually in Excel

relData <- read.delim(file = "rel_abundance_allMAGS_long_from_R_for_NMDS.txt", header = TRUE, sep = "\t")
str(relData)
head(relData)
dim(relData)

relData$Researcher <- as.factor(relData$Researcher)
relData$Researcher_Reactor <- as.factor(relData$Researcher_Reactor)
relData$Sample_Name <- as.factor(relData$Sample_Name)
relData$Seq_Tech <- as.factor(relData$Seq_Tech)
relData$MAG_ID <- as.factor(relData$MAG_ID)
str(relData)
head(relData)
dim(relData)

plot_Data <- relData %>%
  select(Researcher, Researcher_Reactor, Sample_Name, Day, Seq_Tech, MAG_ID, Relative_Abundance) %>%
  tidyr::spread(MAG_ID, Relative_Abundance)

dim(plot_Data)

beta_dist <- vegdist(plot_Data[,6:136], index = "bray")
beta_dist

nmds <- metaMDS(beta_dist)
nmds_data <- as.data.frame(nmds$points)
nmds_data$Sample_Name <- plot_Data$Sample_Name
nmds_data <- dplyr::left_join(nmds_data, plot_Data)

ggplot()+
  geom_text(data=nmds_data, aes(x=MDS1,y=MDS2,label=Day,color=Researcher_Reactor), size=4, nudge_x=0.1) +
  geom_point(data=nmds_data, aes(x=MDS1,y=MDS2,color=Researcher_Reactor), size=2) +
  geom_polygon(data=nmds_data, aes(x=MDS1,y=MDS2,fill=Researcher_Reactor, group=Researcher_Reactor), alpha = 0.2) +
  coord_equal() +
  theme_bw() +
  scale_color_manual(values = c("red", "black", "chocolate1", "orangered1",
                                "green", "green4", "cornflowerblue", "mediumblue",
                                "blueviolet", "darkorchid1", "violetred")) +
  labs(title = "NMDS Plot for all Representative Genomes - Reactor Separated") +
  theme(panel.background = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        plot.background = element_blank(),
        plot.title = element_text())

plot(nmds)
ordiellipse(nmds, groups=nmds_data$Researcher_Reactor, kinds = "sd")

#combine plots in illustrator

#perform PERMANOVA to compare reactors
#https://data.marcoplebani.com/annotated-code-for-performing-multivariate-statistics/

if (!require(pairwiseAdonis)) install_github("pmartinezarbizu/pairwiseAdonis/pairwiseAdonis")
library(pairwiseAdonis)

nmds.obs <- nmds_data[8:78]
nmds.spp <- data.frame(Reactor=nmds_data$Researcher_Reactor)
nmds.manova <- adonis2(nmds.obs ~ Reactor, method = "euclidean", data = nmds.spp)
nmds.manova

nmds.adonis.pw <- pairwise.adonis(x=nmds.obs, factors = nmds.spp$Reactor, sim.method = "euclidean", p.adjust.m="BH")
nmds.adonis.pw <- as.data.frame(nmds.adonis.pw)
nmds.adonis.pw$F.Model <- round(nmds.adonis.pw$F.Model,2)
nmds.adonis.pw$R2 <- round(nmds.adonis.pw$R2, 2)
nmds.adonis.pw

write.table(file = "Post_hoc_PERMNOVA_results_euc_dist_BH_correction.txt", nmds.adonis.pw, sep = "\t", col.names = F, quote = F)
