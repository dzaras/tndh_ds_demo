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
df1a <- read_csv('extracted_variables_from_SUDORS_narratives_2019-2022_11-28-22.csv')

## Now, I will import the cases from the folders 10.03.22 and 11.07.22 on the Z: drive
df1b <- read_csv('extracted_variables_from_SUDORS_narratives_10.03.22_11.07.22.csv')

# Concatenate the two dataframes df1a and df1b
df1c <- rbind(df1a, df1b)

df1c$DID <- as.numeric(df1c$DID)  # convert to numeric so that there are no issues with the joining dataframes

## import list of DIDs provided on 11/28/22 that are to be imported to REDCAP
df2 <- read_csv('C:/Users/DC20B46/Downloads/DIDs_to_scrape_import.csv')

df2$DID <- df2$did  # create a new column 'DID' to match the name of the column in the df1 dataframe
df2 = subset(df2, select = -c(did)) # drop column 'did' for clarity

df3 <- left_join(df2, df1c, by = "DID")  # Apply left_join to keep only data that match DIDs from df2

sum(is.na(df3$...1))  # Only 1 NA after concatenating df1a and df1b - when joining only df1a we had 213 NAs 
sum(is.na(df3$year))  # 1 NA
sum(is.na(df3$hxfentanyl)) # 18 NAs
sum(is.na(df3$narr)) # 28 NAs - so even if we upload 492 cases, we might really have 482

## So, we seem to have 280 cases for which we have values that we can upload to REDCAP 
## (510 observations in df3 - 230 rows with NAs)

which(df3$cme_suicideattempthistory==1)

df3[123,]

write.csv(df3, 'C:/Users/DC20B46/Documents/extracted_variables_combined_until_11.07.22.csv', row.names=F)



