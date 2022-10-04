## Author: Dimitrios Zaras
## Project: Update Forensic Center Information on RedCap for 2020 autopsies

## Date Created: 9/26/22
## Purpose of this file:
## This file takes the raw data about forensic centers from SUDORS autopsy reports
## from 2020 and pushes it on to RedCap

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
                       verbose = TRUE,
                       fields = "did")$data
                       #filter_logic = paste0("[report_period] = '", reporting, "'"))$data
      
dim(RC_DIDS)
head(RC_DIDS)


## Import extracted data from local drive
df <- read_csv('narratives_sudors_2019-2022_09.02.22.csv')
head(df)

## keep only the "DID" and "forensic_center" columns from the imported data to later merge with the 
## dataframe that I downloaded from RedCap
drop <- c("DID","forensic_center")
df2 = df[,(names(df) %in% drop)]

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
                                                   'S' = '3',
                                                   'E' = '4',
                                                   'N' = '5')

df_for_rc$name_of_regional_forensic <- as.factor(df_for_rc$name_of_regional_forensic)
levels(df_for_rc$name_of_regional_forensic)

# take first ten rows for testing 
df_for_rc_test <- df_for_rc[1:10,]
names(df_for_rc_test)[names(df_for_rc_test) == 'forensic_center'] <- 'name_of_regional_forensic'


# df_for_rc$name_of_regional_forensic <- as.factor(df_for_rc$name_of_regional_forensic)
# levels(df_for_rc$name_of_regional_forensic)

###
# df_for_rc_test$name_of_regional_forensic <- recode(df_for_rc_test$name_of_regional_forensic, 
#                         W = 'West Tennessee Regional Forensic Center (West)', 
#                         M = 'Center for Forensic Medicine (Middle)',
#                         SE = 'Hamilton County Forensic Center (Southeast)',
#                         E = 'Knox County Regional Forensic Center (East)',
#                         NE = 'William L.Jenkins Forensic Center, ETSU (Northeast)')


df_for_rc_test$name_of_regional_forensic <- recode(df_for_rc_test$name_of_regional_forensic, 
                                 'West' = 1, 
                                'Middle' = 2,
                                'Southeast' = 3,
                                'East' = 4,
                                'Northeast' = 5)


levels(df_for_rc_test$name_of_regional_forensic)

#df_for_rc_test$name_of_regional_forensic <- factor(df_for_rc_test$name_of_regional_forensic, levels =
#                                                     c(levels(df_for_rc_test$name_of_regional_forensic), "Knox County Regional Forensic Center (East)"))

#df_for_rc_test$name_of_regional_forensic <- factor(df_for_rc_test$name_of_regional_forensic, levels =
#                                                     c(levels(df_for_rc_test$name_of_regional_forensic), "West Tennessee Regional Forensic Center (West)"))

levels(df_for_rc_test$name_of_regional_forensic)

# init_cases <- df_for_rc %>%
#   select(did) %>%
#   mutate(forensic_center = 0) 

# Write to redcap
redcap_write_oneshot(ds = init_cases, 
                     redcap_uri = uri, 
                     token = token)

redcap_write_oneshot(ds = df_for_rc_test, 
                     redcap_uri = uri, 
                     token = token)






