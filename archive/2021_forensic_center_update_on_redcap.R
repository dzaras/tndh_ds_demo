## Author: Dimitrios Zaras
## Project: Update Forensic Center Information on RedCap for 2021 autopsies

## Date Created: 9/27/22
## Purpose of this file:
## This file takes the raw data about forensic centers from SUDORS autopsy reports
## from 2021 and pushes it on to RedCap

library(REDCapR)
library(RODBC)
library(tidyverse)
library(lubridate)

# Set working directory
setwd('C:/Users/DC20B46/Documents')

### RedCAP info

token <- "4E9279E00A9EFFD03CFDAA0ACCAC1669"  # for the project SUDORS Current Abstraction
# token <- "F11182BE4FF8580C3217D522B21C2EED"  # for the SUDORS Testing project   

uri='https://tdhrc.health.tn.gov/redcap/api/'

## Import initial data
## List of available RedCAP variables
metadat <- redcap_metadata_read(token = token, redcap_uri = uri)$data

variable.names(metadat)

## List of current DIDs in RedCAP 
RC_DIDS <- redcap_read(redcap_uri = uri,
                       token = token,
                       verbose = FALSE,
                       fields = "did")$data
#filter_logic = paste0("[report_period] = '", reporting, "'"))$data

dim(RC_DIDS)
head(RC_DIDS)

# find matches for DIDs that start with 2021 from the downloaded data from RedCap
#grep("2021", RC_DIDS$did, value = TRUE, ignore.case = TRUE)
class(RC_DIDS$did)

#sort(RC_DIDS$did)

# RC_DIDS$did <- toString(RC_DIDS$did)
years_list <- substr(RC_DIDS$did, 1, 4) # first 4 digits of DID show the year
years_list <- as.integer(years_list)
table(years_list) # 3,954 values of '2021' 


## Import extracted data from local drive
df <- read_csv('narratives_sudors_2019-2022_09.02.22.csv')
head(df)

# keep only records from 2021 - as a first step of importing the data on redcap 
df21 = df[df$year == 2021,]

## keep only the "DID" and "forensic_center" columns from the imported data to later merge with the 
## dataframe that I downloaded from RedCap
drop <- c("DID","forensic_center")
df2 = df21[,(names(df) %in% drop)]


## rename DID to did to match the column name in the RC_DIDS dataframe
names(df2)[names(df2) == 'DID'] <- 'did'

glimpse(df2)

## join the two dataframes based on common DIDS
df_for_rc = merge(x = RC_DIDS, y = df2, by = "did")

glimpse(df_for_rc)

# drop2 <- c("status","dc_autocompl", "number_pharmacies_180")
# df_for_rc = df_for_rc[,!(names(df_for_rc) %in% drop2)]


## find duplicates in the df_for_rc dataframe
which(duplicated(df_for_rc))

df_for_rc <- unique(df_for_rc)
dim(df_for_rc)

# Push forensic center data to RedCAP

# Write to redcap
names(df_for_rc)[names(df_for_rc) == 'forensic_center'] <- 'name_of_regional_forensic'

df_for_rc$name_of_regional_forensic <- recode(df_for_rc$name_of_regional_forensic, 
                                              'W' = '1', 
                                              'M' = '2',
                                              'SE' = '3',
                                              'E' = '4',
                                              'NE' = '5')

df_for_rc$name_of_regional_forensic <- as.factor(df_for_rc$name_of_regional_forensic)
levels(df_for_rc$name_of_regional_forensic)

###
# df_for_rc_test$name_of_regional_forensic <- recode(df_for_rc_test$name_of_regional_forensic, 
#                         W = 'West Tennessee Regional Forensic Center (West)', 
#                         M = 'Center for Forensic Medicine (Middle)',
#                         SE = 'Hamilton County Forensic Center (Southeast)',
#                         E = 'Knox County Regional Forensic Center (East)',
#                         NE = 'William L.Jenkins Forensic Center, ETSU (Northeast)')



# init_cases <- df_for_rc %>%
#   select(did) %>%
#   mutate(forensic_center = 0) 

# Write to redcap
redcap_write_oneshot(ds = init_cases, 
                     redcap_uri = uri, 
                     token = token)

redcap_write_oneshot(ds = df_for_rc, 
                     redcap_uri = uri, 
                     token = token)

head(df_for_rc, 20)





