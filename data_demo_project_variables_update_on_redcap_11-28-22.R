## Author: Dimitrios Zaras
## Project: Update Data Demonstration Variables on RedCap for 2022 autopsies

## Date Created: 11/22/2022
## Purpose of this file:
## This file takes the raw data about various variables of interest from SUDORS autopsy reports
## from 2022 and pushes it on to RedCap

library(REDCapR)
library(RODBC)
library(tidyverse)
library(lubridate)
library(tidyr)
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
df3 <- read_csv('C:/Users/DC20B46/Documents/extracted_variables_combined_until_11.07.22.csv')
### I will use df3 from the joining dids to upload to redcap script because I'm currently having trouble
### saving that dataframe in windows 
head(df3)
table(df3$year)

# forensic center variable
names(df3)[names(df3) == 'forensic_center'] <- 'name_of_regional_forensic'

df3$name_of_regional_forensic <- as.factor(df3$name_of_regional_forensic)
levels(df3$name_of_regional_forensic)

###
df3$name_of_regional_forensic <- recode(df3$name_of_regional_forensic, 
                                       'W' = '1', 
                                       'M' = '2',
                                       'SE' = '3',
                                       'E' = '4',
                                       'NE' = '5')

# create a new variable in the df to import the information related to the 'OD' tab on REDCap

# assign values to the current_past_misuse variable categories
df3$current_past_misuse___1 <- factor(NA, levels = c(0,1))  # current_past_misuse___1

df3$current_past_misuse___1[df3$hxheroin==0 & df3$hxrxopioid==0 & df3$hxanyopioid==0 &
                             df3$hxfentanyl==0 & df3$hxcocaine==0 & df3$hxmeth==0 & df3$hxbenzo==0 & df3$hxcannabis==0 & 
                             df3$hxunspecified == 0]<- 1

df3$current_past_misuse___1[df3$hxheroin==1 | df3$hxrxopioid==1 | df3$hxanyopioid==1 |
                             df3$hxfentanyl==1 | df3$hxcocaine==1 | df3$hxmeth==1 | df3$hxbenzo==1 |
                             df3$hxcannabis==1 | df3$hxunspecified == 1]<- 0 

df3$current_past_misuse___2 <- factor(NA, levels = c(0, 1))

df3$current_past_misuse___2[df3$hxheroin == 1]<- 1   # "current_past_misuse___2"
df3$current_past_misuse___2[df3$hxheroin == 0]<- 0   # 

df3$current_past_misuse___3 <- factor(NA, levels = c(0, 1))

df3$current_past_misuse___3[df3$hxrxopioid == 1]<- 1 # "current_past_misuse___3"
df3$current_past_misuse___3[df3$hxrxopioid == 0]<- 0

df3$current_past_misuse___4 <- factor(NA, levels = c(0,1))

df3$current_past_misuse___4[df3$hxanyopioid == 1]<- 1 # "current_past_misuse___4"
df3$current_past_misuse___4[df3$hxanyopioid == 0]<- 0

df3$current_past_misuse___5 <- factor(NA, levels = c(0,1))

df3$current_past_misuse___5[df3$hxfentanyl == 1]<- 1 # "current_past_misuse___5"
df3$current_past_misuse___5[df3$hxfentanyl == 0]<- 0

df3$current_past_misuse___6 <- factor(NA, levels = c(0,1))

df3$current_past_misuse___6[df3$hxcocaine == 1]<- 1 # "current_past_misuse___6"
df3$current_past_misuse___6[df3$hxcocaine == 0]<- 0 

df3$current_past_misuse___7 <- factor(NA, levels = c(0,1))

df3$current_past_misuse___7[df3$hxmeth == 1]<- 1 # "current_past_misuse___7"
df3$current_past_misuse___7[df3$hxmeth == 0]<- 0

df3$current_past_misuse___8 <- factor(NA, levels = c(0,1))

df3$current_past_misuse___8[df3$hxbenzo == 1]<- 1 # "current_past_misuse___8"
df3$current_past_misuse___8[df3$hxbenzo == 0]<- 0

df3$current_past_misuse___9 <- factor(NA, levels = c(0,1))

df3$current_past_misuse___9[df3$hxcannabis == 1]<- 1 # "current_past_misuse___9"
df3$current_past_misuse___9[df3$hxcannabis == 0]<- 0

df3$current_past_misuse___10 <- factor(NA, levels = c(0,1))

df3$current_past_misuse___10[df3$hxunspecified == 1]<- 1 # "current_past_misuse___10"
df3$current_past_misuse___10[df3$hxunspecified == 0]<- 0


# adding a new column to the df dataframe to check if that fixes the error message when importing to RC
# df$hxothersubstancespecify <- 0
# df$current_past_misuse[df$hxothersubstancespecify == 1]<- 11 # "current_past_misuse___10"

# Create new variable in the df to import the information from the 'Any evidence of drug use' from the word
# document or 'evddrug' from the pdf codebook or 'indicationsdrugspara' variables - which are all the same
df3$evddrug <- factor(NA, levels = c(1, 2))

# assign values to the evddrug levels
df3$evddrug[df3$indicationsdrugpara == 1] <- 1

df3$evddrug[df3$indicationsdrugpara == 0] <- 2

# non-specific evidence of drug use
df3$non_specific_evidence___1 <- factor(NA, levels = c(0,1))

df3$non_specific_evidence___1[df3$non_specific_evidence == 1] <- 1
df3$non_specific_evidence___1[df3$non_specific_evidence == 0] <- 0


# Create new variable for "Smoke" from the word document, smoke from pdf3 codebook
df3$smoke___1 <- factor(NA, levels = c(0, 1))

df3$smoke___1[df3$hasroutesmoking == 1] <- 1
df3$smoke___1[df3$hasroutesmoking == 0] <- 0

# Create smoke_evidence variable
df3$smoke_evidence___1 <- factor(NA,levels = c(0, 1))

df3$smoke_evidence___1[df3$smokingpipe == 0] <- 0
df3$smoke_evidence___1[df3$smokingpipe == 1]<- 1   # 

df3$smoke_evidence___2 <- factor(NA, levels= c(0,1))

df3$smoke_evidence___2[df3$smokingtinfoil == 0] <- 0
df3$smoke_evidence___2[df3$smokingtinfoil == 1]<- 1 

df3$smoke_evidence___3 <- factor(NA, levels = c(0,1))

df3$smoke_evidence___3[df3$smokingvape == 0]<- 0
df3$smoke_evidence___3[df3$smokingvape == 1]<- 1

df3$smoke_evidence___4 <- factor(NA, levels = c(0,1))

df3$smoke_evidence___4[df3$smokingbongbowl == 0]<- 0 
df3$smoke_evidence___4[df3$smokingbongbowl == 1]<- 1 

# create evidence of injection variable
df3$evidenceofinjection___1 <- factor(NA, c(0,1))

df3$evidenceofinjection___1[df3$routeinjection == 1] <- 1
df3$evidenceofinjection___1[df3$routeinjection == 0] <- 0

# create injection evidence variable
df3$injection_evidence___1 <- factor(NA,levels = c(0, 1))

df3$injection_evidence___1[df3$indicationstracks == 0] <- 0
df3$injection_evidence___1[df3$indicationstracks == 1]<- 1   # 

df3$injection_evidence___2 <- factor(NA, levels= c(0,1))

df3$injection_evidence___2[df3$hasevidenceofinjectiontourni == 0] <- 0
df3$injection_evidence___2[df3$hasevidenceofinjectiontourni == 1]<- 1 

df3$injection_evidence___3 <- factor(NA, levels = c(0,1))

df3$injection_evidence___3[df3$hasevidenceofinjectioncooker == 0]<- 0
df3$injection_evidence___3[df3$hasevidenceofinjectioncooker == 1]<- 1

df3$injection_evidence___4 <- factor(NA, levels = c(0,1)) # this is the varialbe related to 'needle' 

df3$injection_evidence___4[df3$hasevidenceofinjectionneedle == 0]<- 0 
df3$injection_evidence___4[df3$hasevidenceofinjectionneedle == 1]<- 1 

df3$injection_evidence___5 <- factor(NA, levels = c(0,1))

df3$injection_evidence___5[df3$hasevidenceofinjectionfilters == 0]<- 0
df3$injection_evidence___5[df3$hasevidenceofinjectionfilters == 1]<- 1

# filters is not among the extracted variables we have collected data for  

# evidence of snorting/sniffing variable
df3$snort_sniff___1 <- factor(NA, levels = c(0, 1))

df3$snort_sniff___1[df3$evidence_of_snorting_sniffing == 1] <- 1
df3$snort_sniff___1[df3$evidence_of_snorting_sniffing == 0] <- 0

# snorting/sniffing evidence variable
df3$snort_sniff_evidence___1 <- factor(NA,levels = c(0, 1))

df3$snort_sniff_evidence___1[df3$straws == 0] <- 0
df3$snort_sniff_evidence___1[df3$straws == 1]<- 1   # 

df3$snort_sniff_evidence___2 <- factor(NA,levels = c(0, 1))

df3$snort_sniff_evidence___2[df3$rolled_paper_or_dollar_bills == 0] <- 0
df3$snort_sniff_evidence___2[df3$rolled_paper_or_dollar_bills == 1]<- 1 

df3$snort_sniff_evidence___3 <- factor(NA,levels = c(0, 1))

df3$snort_sniff_evidence___3[df3$razor_blades == 0] <- 0
df3$snort_sniff_evidence___3[df3$razor_blades == 1]<- 1 

df3$snort_sniff_evidence___4 <- factor(NA,levels = c(0, 1))

df3$snort_sniff_evidence___4[df3$powder_on_table_mirror == 0] <- 0
df3$snort_sniff_evidence___4[df3$powder_on_table_mirror == 1]<- 1 

df3$snort_sniff_evidence___5 <- factor(NA, levels= c(0,1))

df3$snort_sniff_evidence___5[df3$snortingpowdernose == 0] <- 0
df3$snort_sniff_evidence___5[df3$snortingpowdernose == 1]<- 1 

# evidence illicit drug  variable

df3$evidence_illicit_drug___1 <- factor(NA, c(0,1))

df3$evidence_illicit_drug___1[df3$illicit_drug_evidence == 0] <- 0
df3$evidence_illicit_drug___1[df3$illicit_drug_evidence == 1]<- 1 

# illicit drug evidence variables

df3$illicit_drugs_evidence___1 <- factor(NA, c(0,1))

df3$illicit_drugs_evidence___1[df3$hasevidenceofillicitpowder == 1] <- 1
df3$illicit_drugs_evidence___1[df3$hasevidenceofillicitpowder == 0] <- 0

df3$illicit_drugs_evidence___2 <- factor(NA, c(0,1))

df3$illicit_drugs_evidence___2[df3$hasevidenceofillicittar == 1] <- 1
df3$illicit_drugs_evidence___2[df3$hasevidenceofillicittar == 0] <- 0

df3$illicit_drugs_evidence___4 <- factor(NA, c(0,1))

df3$illicit_drugs_evidence___4[df3$hasevidenceofillicitcrystal == 1] <- 1
df3$illicit_drugs_evidence___4[df3$hasevidenceofillicitcrystal == 0] <- 0

df3$illicit_drugs_evidence___6 <- factor(NA, c(0,1))

df3$illicit_drugs_evidence___6[df3$hasevidenceofillicitpackage == 1] <- 1
df3$illicit_drugs_evidence___6[df3$hasevidenceofillicitpackage == 0] <- 0

# create know medical conditions variable
df3$known_medical_conditions___1 <- factor(NA, c(0,1))

df3$known_medical_conditions___1[df3$medhx_COPD == 0] <- 0
df3$known_medical_conditions___1[df3$medhx_COPD == 1]<- 1 

df3$known_medical_conditions___2 <- factor(NA, c(0,1))

df3$known_medical_conditions___2[df3$medhx_asthma == 0] <- 0
df3$known_medical_conditions___2[df3$medhx_asthma == 1]<- 1 

df3$known_medical_conditions___3 <- factor(NA, c(0,1))

df3$known_medical_conditions___3[df3$medhx_apnea == 0] <- 0
df3$known_medical_conditions___3[df3$medhx_apnea == 1]<- 1 

df3$known_medical_conditions___4 <- factor(NA, c(0,1))

df3$known_medical_conditions___4[df3$medhx_heart == 0] <- 0
df3$known_medical_conditions___4[df3$medhx_heart == 1]<- 1 

df3$known_medical_conditions___5 <- factor(NA, c(0,1))

df3$known_medical_conditions___5[df3$medhx_obesity == 0] <- 0
df3$known_medical_conditions___5[df3$medhx_obesity == 1]<- 1 

df3$known_medical_conditions___7 <- factor(NA, c(0,1))

df3$known_medical_conditions___7[df3$medhx_migraine == 0] <- 0
df3$known_medical_conditions___7[df3$medhx_migraine == 1]<- 1

df3$known_medical_conditions___8 <- factor(NA, c(0,1))

df3$known_medical_conditions___8[df3$medhx_backpain == 0] <- 0
df3$known_medical_conditions___8[df3$medhx_backpain == 1]<- 1

df3$known_medical_conditions___9 <- factor(NA, c(0,1))

df3$known_medical_conditions___9[df3$medhx_hepc == 0] <- 0
df3$known_medical_conditions___9[df3$medhx_hepc == 1]<- 1

df3$known_medical_conditions___10 <- factor(NA, c(0,1))

df3$known_medical_conditions___10[df3$medhx_hiv == 0] <- 0
df3$known_medical_conditions___10[df3$medhx_hiv == 1]<- 1

df3$known_medical_conditions___11 <- factor(NA, c(0,1))

df3$known_medical_conditions___11[df3$medhx_otherpain == 0] <- 0
df3$known_medical_conditions___11[df3$medhx_otherpain == 1]<- 1

df3$known_medical_conditions___12 <- factor(NA, c(0,1))

df3$known_medical_conditions___12[df3$medhx_otherbreathing == 0] <- 0
df3$known_medical_conditions___12[df3$medhx_otherbreathing == 1]<- 1

# 'Circumastances' tab on REDCap

# cme_substanceabuseother
df3$cme_substanceabuseother___1 <- factor(NA, levels = c(1,0))

df3$cme_substanceabuseother___1[df3$cme_substanceabuseother == 0] <- 0
df3$cme_substanceabuseother___1[df3$cme_substanceabuseother == 1] <- 1

# cme_alcoholproblem
df3$cme_alcoholproblem___1 <- factor(NA, levels= c(1,0))

df3$cme_alcoholproblem___1[df3$cme_alcoholproblem == 0] <- 0
df3$cme_alcoholproblem___1[df3$cme_alcoholproblem == 1] <- 1

# Cme_mentalhealthproblem
df3$cme_mentalhealthproblem___1 <- factor(NA, levels= c(1,0))

df3$cme_mentalhealthproblem___1[df3$cme_mentalhealthproblem == 0] <- 0
df3$cme_mentalhealthproblem___1[df3$cme_mentalhealthproblem == 1] <- 1

# cme_traumatic brain injury - tbi
df3$cme_tbi___1 <- factor(NA, c(0,1))

df3$cme_tbi___1[df3$cme_istraumaticbraininjuryhist == 0] <- 0
df3$cme_tbi___1[df3$cme_istraumaticbraininjuryhist == 1] <- 1

# Cme_suicide attempt history
df3$cme_suicideattempthistory___1 <- factor(NA, c(0,1))

df3$cme_suicideattempthistory___1[df3$cme_suicideattempthistory == 0] <- 0
df3$cme_suicideattempthistory___1[df3$cme_suicideattempthistory == 1] <- 1

# cme_suicide thought history
df3$cme_suicidethoughthistory___1 <- factor(NA, c(0,1))

df3$cme_suicidethoughthistory___1[df3$cme_suicidethoughthistory == 0] <- 0
df3$cme_suicidethoughthistory___1[df3$cme_suicidethoughthistory == 1] <- 1

## keep only the "DID" and "current_past_misuse" columns from the imported data to later merge with the 
## dataframe that I downloaded from RedCap
drop <- c("DID", "name_of_regional_forensic",
          "evddrug","non_specific_evidence___1",
          "current_past_misuse___1", "current_past_misuse___2","current_past_misuse___3", "current_past_misuse___4",
          "current_past_misuse___5", "current_past_misuse___6","current_past_misuse___7","current_past_misuse___8",
          "current_past_misuse___9","current_past_misuse___10", 
          "smoke___1","smoke_evidence___1", "smoke_evidence___2", "smoke_evidence___3","smoke_evidence___4",
          "evidenceofinjection___1", "injection_evidence___1","injection_evidence___2","injection_evidence___3", 
          "injection_evidence___4", "injection_evidence___5",
          "snort_sniff___1", "snort_sniff_evidence___1" ,"snort_sniff_evidence___2", "snort_sniff_evidence___3", "snort_sniff_evidence___4", "snort_sniff_evidence___5",
          "evidence_illicit_drug___1","evidence_illicit_drug___1",
          "illicit_drugs_evidence___1","illicit_drugs_evidence___2","illicit_drugs_evidence___4",
          "illicit_drugs_evidence___6",
          "known_medical_conditions___1","known_medical_conditions___2","known_medical_conditions___3",
          "known_medical_conditions___4","known_medical_conditions___5",
          "known_medical_conditions___7","known_medical_conditions___8","known_medical_conditions___9",
          "known_medical_conditions___10","known_medical_conditions___11","known_medical_conditions___12",
          "cme_substanceabuseother___1","cme_alcoholproblem___1","cme_mentalhealthproblem___1",
          "cme_tbi___1", "cme_suicideattempthistory___1","cme_suicidethoughthistory___1"
)

df4 = df3[,(names(df3) %in% drop)]


## rename DID to did to match the column name in the RC_DIDS dataframe
names(df4)[names(df4) == 'DID'] <- 'did'

glimpse(df4)

## getting rid of the cases from the df4 dataframe that have NA values 
sum(is.na(df4$current_past_misuse___1)) # 18 NAs
df5 <- df4

df5 <- df5[!is.na(df5$current_past_misuse___1),]

## join the two dataframes based on common DIDS
df_for_rc = merge(x = RC_DIDS, y = df5, by = "did")

glimpse(df_for_rc)

# drop2 <- c("status","dc_autocompl", "number_pharmacies_180")
# df_for_rc = df_for_rc[,!(names(df_for_rc) %in% drop2)]


## find duplicates in the df_for_rc dataframe
which(duplicated(df_for_rc))

df_for_rc <- unique(df_for_rc)
dim(df_for_rc)

# first try to upload the current_past_misuse information for autopsies that haven't been abstracted
df_for_rc_b <- df_for_rc[df_for_rc$status == 0,]

# df_for_rc_c <- df_for_rc_b[0:40,]
# DIDs: 2022001797, 2022001434, 2022001793, 2022001802, 2022001844, 2022001865, 2022002026
#keep <-  c("2022001797", "2022001434", "2022001793", "2022001802", "2022001844", "2022001865", "2022002026")

#df_for_rc2 <- subset(df_for_rc, did %in% keep)
#df_for_rc2$did  # print the did's which are not abstracted and for which we have data on current_past_misuse
# "2022001793" "2022001797" "2022001802" "2022001844" "2022001865" "2022002026"

#print(df_for_rc2)

#df_for_rc2 <- df_for_rc2[1,]


#init_cases <- df_for_rc2 %>%
#  select(did) %>%
#   mutate(smoke___1) 

# Write to redcap
#redcap_write_oneshot(ds = init_cases, 
#                     redcap_uri = uri, 
#                     token = token)

redcap_write_oneshot(ds = df_for_rc_b,    # I didn't use df_for_rc_c in this instance because it's not needed 
                     redcap_uri = uri, 
                     token = token)

head(df_for_rc_c, 20)


a <- validate_for_write(df_for_rc_b)
print(a)

