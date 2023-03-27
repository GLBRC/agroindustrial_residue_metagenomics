#plotting NMDS plots for metagenomic data

library(ggplot2)
library(dplyr)
library(cowplot)
library(ggthemes)
library(RColorBrewer)
library(tidyverse)
library(forcats)
library(vegan)

setwd("./example_files")

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
