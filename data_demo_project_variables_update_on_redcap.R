## Author: Dimitrios Zaras
## Project: Update Data Demonstration Variables on RedCap for 2022 autopsies

## Date Created: 10/3/22
## Purpose of this file:
## This file takes the raw data about various variables of interest from SUDORS autopsy reports
## from 2022 and pushes it on to RedCap

library(REDCapR)
library(RODBC)
library(tidyverse)
library(lubridate)
# library(redcapAPI) # check for conflict with REDCapR
library(dplyr)
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
                       fields = c("did", "status"),)$data
                       
#filter_logic = paste0("[report_period] = '", reporting, "'"))$data

dim(RC_DIDS)
head(RC_DIDS)

# find matches for DIDs that start with 2022 from the downloaded data from RedCap
#grep("2022", RC_DIDS$did, value = TRUE, ignore.case = TRUE)
class(RC_DIDS$did)
class(RC_DIDS$status)
#sort(RC_DIDS$did)

# RC_DIDS$did <- toString(RC_DIDS$did)
years_list <- substr(RC_DIDS$did, 1, 4)
years_list <- as.integer(years_list)
table(years_list) # 1,789 values of '2022' as of 10/27/22
table(years_list, RC_DIDS$status) # 1,366 values of 0 for the 'status' variable in 2022 at 10/21/22
# 1,287 values of 0 for the 'status' variable in 2022 at 10/21/22

## Import extracted data from local drive
df <- read_csv('extracted_variables_from_SUDORS_narratives_2022.csv')
head(df)
table(df$year)

# forensic center variable
names(df)[names(df) == 'forensic_center'] <- 'name_of_regional_forensic'

df$name_of_regional_forensic <- as.factor(df$name_of_regional_forensic)
levels(df$name_of_regional_forensic)

###
df$name_of_regional_forensic <- recode(df$name_of_regional_forensic, 
                                       'W' = '1', 
                                       'M' = '2',
                                       'SE' = '3',
                                       'E' = '4',
                                       'NE' = '5')

# create a new variable in the df to import the information related to the 'OD' tab on REDCap

# assign values to the current_past_misuse variable categories
df$current_past_misuse___1 <- factor(NA, levels = c(0,1))  # current_past_misuse___1

df$current_past_misuse___1[df$hxheroin==0 & df$hxrxopioid==0 & df$hxanyopioid==0 &
                         df$hxfentanyl==0 & df$hxcocaine==0 & df$hxmeth==0 & df$hxbenzo==0 & df$hxcannabis==0 & 
                        df$hxunspecified == 0]<- 1

df$current_past_misuse___1[df$hxheroin==1 | df$hxrxopioid==1 | df$hxanyopioid==1 |
                             df$hxfentanyl==1 | df$hxcocaine==1 | df$hxmeth==1 | df$hxbenzo==1 |
                             df$hxcannabis==1 | df$hxunspecified == 1]<- 0 

df$current_past_misuse___2 <- factor(NA, levels = c(0, 1))

df$current_past_misuse___2[df$hxheroin == 1]<- 1   # "current_past_misuse___2"
df$current_past_misuse___2[df$hxheroin == 0]<- 0   # 

df$current_past_misuse___3 <- factor(NA, levels = c(0, 1))

df$current_past_misuse___3[df$hxrxopioid == 1]<- 1 # "current_past_misuse___3"
df$current_past_misuse___3[df$hxrxopioid == 0]<- 0

df$current_past_misuse___4 <- factor(NA, levels = c(0,1))

df$current_past_misuse___4[df$hxanyopioid == 1]<- 1 # "current_past_misuse___4"
df$current_past_misuse___4[df$hxanyopioid == 0]<- 0

df$current_past_misuse___5 <- factor(NA, levels = c(0,1))

df$current_past_misuse___5[df$hxfentanyl == 1]<- 1 # "current_past_misuse___5"
df$current_past_misuse___5[df$hxfentanyl == 0]<- 0

df$current_past_misuse___6 <- factor(NA, levels = c(0,1))

df$current_past_misuse___6[df$hxcocaine == 1]<- 1 # "current_past_misuse___6"
df$current_past_misuse___6[df$hxcocaine == 0]<- 0 

df$current_past_misuse___7 <- factor(NA, levels = c(0,1))

df$current_past_misuse___7[df$hxmeth == 1]<- 1 # "current_past_misuse___7"
df$current_past_misuse___7[df$hxmeth == 0]<- 0

df$current_past_misuse___8 <- factor(NA, levels = c(0,1))

df$current_past_misuse___8[df$hxbenzo == 1]<- 1 # "current_past_misuse___8"
df$current_past_misuse___8[df$hxbenzo == 0]<- 0

df$current_past_misuse___9 <- factor(NA, levels = c(0,1))

df$current_past_misuse___9[df$hxcannabis == 1]<- 1 # "current_past_misuse___9"
df$current_past_misuse___9[df$hxcannabis == 0]<- 0

df$current_past_misuse___10 <- factor(NA, levels = c(0,1))

df$current_past_misuse___10[df$hxunspecified == 1]<- 1 # "current_past_misuse___10"
df$current_past_misuse___10[df$hxunspecified == 0]<- 0


# adding a new column to the df dataframe to check if that fixes the error message when importing to RC
# df$hxothersubstancespecify <- 0
# df$current_past_misuse[df$hxothersubstancespecify == 1]<- 11 # "current_past_misuse___10"

# Create new variable in the df to import the information from the 'Any evidence of drug use' from the word
# document or 'evddrug' from the pdf codebook or 'indicationsdrugspara' variables - which are all the same
df$evddrug <- factor(NA, levels = c(1, 2))

# assign values to the evddrug levels
df$evddrug[df$indicationsdrugpara == 1] <- 1

df$evddrug[df$indicationsdrugpara == 0] <- 2

# non-specific evidence of drug use
df$non_specific_evidence___1 <- factor(NA, levels = c(0,1))

df$non_specific_evidence___1[df$non_specific_evidence == 1] <- 1
df$non_specific_evidence___1[df$non_specific_evidence == 0] <- 0


# Create new variable for "Smoke" from the word document, smoke from pdf codebook
df$smoke___1 <- factor(NA, levels = c(0, 1))

df$smoke___1[df$hasroutesmoking == 1] <- 1
df$smoke___1[df$hasroutesmoking == 0] <- 0

# Create smoke_evidence variable
df$smoke_evidence___1 <- factor(NA,levels = c(0, 1))

df$smoke_evidence___1[df$smokingpipe == 0] <- 0
df$smoke_evidence___1[df$smokingpipe == 1]<- 1   # 

df$smoke_evidence___2 <- factor(NA, levels= c(0,1))

df$smoke_evidence___2[df$smokingtinfoil == 0] <- 0
df$smoke_evidence___2[df$smokingtinfoil == 1]<- 1 

df$smoke_evidence___3 <- factor(NA, levels = c(0,1))

df$smoke_evidence___3[df$smokingvape == 0]<- 0
df$smoke_evidence___3[df$smokingvape == 1]<- 1

df$smoke_evidence___4 <- factor(NA, levels = c(0,1))

df$smoke_evidence___4[df$smokingbongbowl == 0]<- 0 
df$smoke_evidence___4[df$smokingbongbowl == 1]<- 1 

# create evidence of injection variable
df$evidenceofinjection___1 <- factor(NA, c(0,1))

df$evidenceofinjection___1[df$routeinjection == 1] <- 1
df$evidenceofinjection___1[df$routeinjection == 0] <- 0

# create injection evidence variable
df$injection_evidence___1 <- factor(NA,levels = c(0, 1))

df$injection_evidence___1[df$indicationstracks == 0] <- 0
df$injection_evidence___1[df$indicationstracks == 1]<- 1   # 

df$injection_evidence___2 <- factor(NA, levels= c(0,1))

df$injection_evidence___2[df$hasevidenceofinjectiontourni == 0] <- 0
df$injection_evidence___2[df$hasevidenceofinjectiontourni == 1]<- 1 

df$injection_evidence___3 <- factor(NA, levels = c(0,1))

df$injection_evidence___3[df$hasevidenceofinjectioncooker == 0]<- 0
df$injection_evidence___3[df$hasevidenceofinjectioncooker == 1]<- 1

df$injection_evidence___4 <- factor(NA, levels = c(0,1))

df$injection_evidence___4[df$hasevidenceofinjectionneedle == 0]<- 0 
df$injection_evidence___4[df$hasevidenceofinjectionneedle == 1]<- 1 

# filters is not among the extracted variables we have collected data for  

# evidence of snorting/sniffing variable
df$snort_sniff___1 <- factor(NA, levels = c(0, 1))

df$snort_sniff___1[df$evidence_of_snorting_sniffing == 1] <- 1
df$snort_sniff___1[df$evidence_of_snorting_sniffing == 0] <- 0

# snorting/sniffing evidence variable
#df$snort_sniff_evidence___1 <- factor(NA,levels = c(0, 1))

#df$snort_sniff_evidence___1[df$ == 0] <- 0
#df$snort_sniff_evidence___1[df$ == 1]<- 1   # 

df$snort_sniff_evidence___5 <- factor(NA, levels= c(0,1))

df$snort_sniff_evidence___5[df$snortingpowdernose == 0] <- 0
df$snort_sniff_evidence___5[df$snortingpowdernose == 1]<- 1 

#df$injection_evidence___3 <- factor(NA, levels = c(0,1))

#df$injection_evidence___3[df$ == 0]<- 0
#df$injection_evidence___3[df$ == 1]<- 1

#df$injection_evidence___4 <- factor(NA, levels = c(0,1))

#df$injection_evidence___4[df$ == 0]<- 0 
#df$injection_evidence___4[df$ == 1]<- 1

# evidence illicit drug  variable

df$evidence_illicit_drug___1 <- factor(NA, c(0,1))

df$evidence_illicit_drug___1[df$illicit_drug_evidence == 0] <- 0
df$evidence_illicit_drug___1[df$illicit_drug_evidence == 1]<- 1 

# illict drug evidence variables

df$illicit_drugs_evidence___1 <- factor(NA, c(0,1))

df$illicit_drugs_evidence___1[df$hasevidenceofillicitpowder == 1] <- 1
df$illicit_drugs_evidence___1[df$hasevidenceofillicitpowder == 0] <- 0

df$illicit_drugs_evidence___2 <- factor(NA, c(0,1))

df$illicit_drugs_evidence___2[df$hasevidenceofillicittar == 1] <- 1
df$illicit_drugs_evidence___2[df$hasevidenceofillicittar == 0] <- 0

df$illicit_drugs_evidence___4 <- factor(NA, c(0,1))

df$illicit_drugs_evidence___4[df$hasevidenceofillicitcrystal == 1] <- 1
df$illicit_drugs_evidence___4[df$hasevidenceofillicitcrystal == 0] <- 0

df$illicit_drugs_evidence___6 <- factor(NA, c(0,1))

df$illicit_drugs_evidence___6[df$hasevidenceofillicitpackage == 1] <- 1
df$illicit_drugs_evidence___6[df$hasevidenceofillicitpackage == 0] <- 0



# 'Circumastances' tab on REDCap

# cme_substanceabuseother
df$cme_substanceabuseother <- factor(NA, levels = c(1,0))

# cme_alcoholproblem
df$cme_alcoholproblem___1 <- factor(NA, levels= c(1,0))

df$cme_alcoholproblem___1[df$cme_alcoholproblem == 0] <- 0
df$cme_alcoholproblem___1[df$cme_alcoholproblem == 1] <- 1


## keep only the "DID" and "current_past_misuse" columns from the imported data to later merge with the 
## dataframe that I downloaded from RedCap
drop <- c("DID", "name_of_regional_forensic",
          "evddrug","non_specific_evidence___1",
          "current_past_misuse___1", "current_past_misuse___2","current_past_misuse___3", "current_past_misuse___4",
          "current_past_misuse___5", "current_past_misuse___6","current_past_misuse___7","current_past_misuse___8",
          "current_past_misuse___9","current_past_misuse___10", 
          "smoke___1" , "smoke_evidence___1", "smoke_evidence___2", "smoke_evidence___3",
          "smoke_evidence___4",
          "cme_alcoholproblem___1")
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

# first try to upload the current_past_misuse information for autopsies that haven't been abstracted
df_for_rc_b <- df_for_rc[df_for_rc$status == 0,]

df_for_rc_c <- df_for_rc_b[0:20,]
# DIDs: 2022001797, 2022001434, 2022001793, 2022001802, 2022001844, 2022001865, 2022002026
#keep <-  c("2022001797", "2022001434", "2022001793", "2022001802", "2022001844", "2022001865", "2022002026")

#df_for_rc2 <- subset(df_for_rc, did %in% keep)
#df_for_rc2$did  # print the did's which are not abstracted and for which we have data on current_past_misuse
# "2022001793" "2022001797" "2022001802" "2022001844" "2022001865" "2022002026"

#df_for_rc2$did <- "2022001292"
#df_for_rc2$smoke___1 <- 1

#print(df_for_rc2)

#df_for_rc2 <- df_for_rc2[1,]


#init_cases <- df_for_rc2 %>%
#  select(did) %>%
#   mutate(smoke___1) 

# Write to redcap
#redcap_write_oneshot(ds = init_cases, 
#                     redcap_uri = uri, 
#                     token = token)

redcap_write_oneshot(ds = df_for_rc_c, 
                     redcap_uri = uri, 
                     token = token)

head(df_for_rc_c, 20)


a <- validate_for_write(df_for_rc)
print(a)

