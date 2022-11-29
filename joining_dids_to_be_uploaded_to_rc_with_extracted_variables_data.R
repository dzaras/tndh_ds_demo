## Author: Dimitrios Zaras
## Project: Update Data Demonstration Variables on RedCap for 2022 autopsies
## Purpose of this file: Join DIDs to be imported to REDCAP with DIDs
## for which we have extracted variables from SUDORS cases

## This is to allow us to import not-yet-abstracted cases to REDCAP so that the team can check the 
## accuracy of the automatic variable extraction

## Date Created: 11/28/2022

library(tidyverse)
setwd('C:/Users/DC20B46/Documents')

## Import extracted data from local drive
df1 <- read_csv('extracted_variables_from_SUDORS_narratives_2022_11-28-22.csv')

df1$DID <- as.numeric(df1$DID)  # convert to numeric so that there are no issues with the joining dataframes

## import list of DIDs provided on 11/28/22 that are to be imported to REDCAP
df2 <- read_csv('C:/Users/DC20B46/Downloads/DIDs_to_scrape_import.csv')

df2$DID <- df2$did  # create a new column 'DID' to match the name of the column in the df1 dataframe
df2 = subset(df2, select = -c(did)) # drop column 'did' for clarity

df3 <- left_join(df2, df1, by = "DID")  # Apply left_join to keep only data that match DIDs from df2

sum(is.na(df3$...1))  # 213 NAs 
sum(is.na(df3$year))  # 213 NAs
## So, we seem to have 297 cases for which we have values that we can upload to REDCAP 
## (510 observations in df3 - 213 rows with NAs)

write.csv(df3, 'C:/Users/DC20B46/Documents', row.names = F)



