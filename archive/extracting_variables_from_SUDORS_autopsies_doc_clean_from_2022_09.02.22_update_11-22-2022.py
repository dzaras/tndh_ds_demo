#!/usr/bin/env python
# coding: utf-8

# # Extracting redcap Variables from SUDORS Autopsies from doc_clean - the entire text of the autopsy report - from 2019-2022 (09.02.22) 9/16/2022

# In[1]:


import pandas as pd
import numpy as np
import os
import re
import copy
os.chdir("C:/Users/DC20B46/Documents")


# In[2]:


# read in the narr_df file where we have the scraped narratives from the autopsy reports
# narr_df = pd.read_csv (r'C:\Users\DC20B46\Documents\narr_df.csv') # this was the file used to develop this script
narr_df = pd.read_feather(r'C:\Users\DC20B46\Documents\narratives_sudors_2019-2022_09.02.22.feather') # data from '19-'22


# In[3]:


narr_df.columns


# In[4]:


narr_df['year'] = narr_df['year'].astype(int)


# In[5]:


narr_df.year.value_counts()


# ## Lists of terms associated with SUDORS variables
# 
# ## Update 11/22/22: Added terms related to heart disease for known medical conditions
# ## Also, added terms that include the word 'use' instead of 'abuse' for the Current or Past History of Use variable in the OD tab
# 
# ### Update 9/16/22: Added lists of paraphernalia-specific terms 
# 
# ### Replaced the double quotation marks for all of the terms in these lists, otherwise the terms were not matched by the functions

# In[6]:


forensic_center_bigrams = ["west tennessee regional forensic science center", "center for forensic medicine",
                   "hamilton county corensic center", "knox county regional forensic center",
                   "william l. jenkins forensic center, etsu"
                  ]

history_of_drug_use_terms_bigrams = ["heroin abuse", "heroin use", "opiod abuse", "opiod use",
                                     "pain med abuse", "pain med use", "pain pill abuse", "pain pill use",                    "opiod abuse", "fentanyl abuse", "cocaine abuse", "crack/cockaine abuse", 
                             "meth abuse","meth use", "methamphetamine abuse", "methamphetamine use",
                                     "methamphetamine intoxication","meth use",
                              "abuse xanax", "benzo abuse", "benzo use", "marijuana abuse", "marijuana use",
                             "history of drug abuse","history of drug use", "medication abuse", "polysubstance abuse",
                                     "polysubstance use"
                            ]

other_substance_abuse_bigrams = ["heroin abuse", "cocaine abuse", "methamphetamine abuse", "history of drug abuse",
                         "medication abuse", "opioid abuse", "pain med abuse", "pain pill abuse", "marijuana abuse",
                         "polysubstance abuse", "substance abuse"
                          ]

history_of_alcohol_abuse_bigrams = [ "alcohol abuse", "heavy drinking", "heavy drinker", "alcohol use"]

mental_health_condition_bigrams = ["depression", "dysthymia", "bipolar", "schizophrenia", "anxiety", 
                           "post-traumatic stress disorder", "ptsd", "add", "adhd", "hyperactivity", 
                           "attention-deficit disorder", "eating disorder", "obsessive-compulsive",
                           "ocd", "mood disorder", "multiple personalities", "fetal alcohol syndrome", "dementia",
                           "down syndrome"]

traumatic_brain_injury_bigrams = ["traumatic brain injury", "tbi"]

suicide_attempts_bigrams = ["suicide attempt"]

suicide_ideation_bigrams = ["suicidal ideation", "thoughts of suicide"]

any_evidence_of_drug_use_bigrams = [ "drug paraphernalia", "uncapped syringe", "syringe cap", "needle cap", "syringe",
                            "needle", "glass pipe", "puncture mark", "puncture wound", "track marks", "tourniquet",
                            "burnt spoon", "spoon", "cotton", "razor blades", "cut straws", "straws", "rolled paper",
                            "dollar bills”, “powder on mirror”, “powder on table”, “powder on nose”, “pipe”, “tinfoil",
                            "fentanyl patch", "pill", "tablet", "prescription bottles", "powder", "powdery substance",
                            "white powdery substance", "crystal", "rock-like substance", "plastic baggies", "baggies",
                            "crushed pills", "grinding device", "prescription bottle", "green leafy substance"
                             ]

non_specific_evidence_bigrams = [ "drug paraphernalia", "evidence of drug use"]
                         
evidence_of_injection_bigrams = [ "puncture mark", "puncture wound", "track marks", "tourniquet", "belt", "burnt spoon",
                         "spoon", "cotton", "uncapped syringe", "syringe cap", "needle cap", "syringe", "needle"
                        ]

evidence_of_snorting_sniffing_bigrams = [ "razor blades", "cut straws", "straws", "rolled paper", "dollar bills", 
                                 "powder on mirror", "powder on table", "powder on nose", "rolled paper", 
                                 "mirror with powder", "table with powder", "line of powder"
                                ]

evidence_of_smoking_bigrams = [ "lighter", "pipes", "tinfoil", "vape pens", "e-cigarettes", "bong", "bowl",
                                "copper", "chore boy", "grinding device", "green leafy substance"]

illicit_drug_evidence_bigrams = [ "powder", "crystal", "rock-like substance", "plastic baggies", "baggies", 
                         "white powdery substance", "powdery substance", "black tar", "tar", "crystal", 
                         "rock like substance", "baggies"
                        ]

relationship_status_bigrams = [ "girlfriend", "boyfriend", "partner", "significant other", "intimate partner",
                              "husband", "wife"]

known_medical_conditions_bigrams = [ "copd", "chronic obstructive pulmonary disease", "asthma", "sleep apnea", 
                                    "heart disease", "hypertension", "high blood pressure", "cardiovascular disease", 
                                    "coronary artery disease", "atherosclerotic cardiovascular disease",
                                    "congestive heart failure", "obesity", "obese",
                                    "migraines", "back pain", "pain in back", "lower back pain", "hep c", 
                                    "hepatitis c", "hiv", "aids", "human immunodeficiency virus", 
                                    "pain", "acute pain", "emphysema", "lung cancer"
                                    ]

### Replaced the variable names (after the first few ones) with their SUDORS variable names as they appear in 
### the redcap_variable_count_check spreadsheet - instead of the names I had used in the previous version of this script

# subcategories of drug paraphernalia groupings based on RedCap Variables
    # _674_current_past_misuse
hxheroin = ["heroin abuse"]
hxrxopioid = ["opioid abuse", "pain med abuse", "pain pill abuse"]
hxanyopioid = ["opioid abuse"]
hxfentanyl = ["fentanyl abuse"]
hxcocaine = ["cocaine abuse", "crack/cocaine abuse", "crack", "cocaine use"]
hxmeth = ["meth abuse", "methamphetamine abuse", "meth use", "methamphetamine abuse"]
hxbenzo = ["abuse xanax"]
hxcannabis = ["marijuana abuse"]
hxunspecified = ["history of drug abuse", "history of drug use", "medication abuse", 
                                             "polysubstance abuse", "substance abuse", "history of substance abuse",
                                             "chronic substance abuse", "iv drug abuse", "intravenous drug abuse",
                                             "known user", "stimulant abuse", "previous overdose", "prior overdose"]
cme_substanceabuseother = ["heroin abuse", "cocaine abuse", "methamphetamine abuse", "history of drug abuse",
                                "medication abuse", "opioid abuse", "pain med abuse", "pain pill abuse", "marijuana abuse",
                                "polysubstance abuse", "substance abuse", "chronic substance abuse", "iv drug abuse",
                                "intravenous drug abuse", "known user", "stimulant abuse", "previous overdose",
                                "prior overdose", "clinical history of"]
cme_alcoholproblem = ["alcohol abuse", "heavy drinking", "heavy drinker", "alcohol use", "alcoholic", 
                           "history of alcoholism", "history of alcohol abuse", "alcoholism"]
cme_mentalhealthproblem = ["depression", "dysthymia", "bipolar", "schizophrenia", "anxiety",
                                "post-traumatic stress disorder", "ptsd", "add", "adhd", "hyperactivity", 
                                "attention-deficit disorder", "eating disorder", "obsessive-compulsive", "ocd",
                                "mood disorder", "multiple personalities", "fetal alcohol syndrome", "dementia",
                                "down syndrome"]
cme_istraumaticbraininjuryhist = ["traumatic brain injury", "tbi"]
cme_suicideattempthistory = ["suicide attempt"]
cme_suicidethoughthistory = ["suicidal ideation", "thoughts of suicide"]
    # _682_evddrug 
indicationsdrugpara = ["“drug paraphernalia", "uncapped syringe", "syringe cap", "needle cap", "syringe",
                               "syringes", "needle", "glass pipe", "puncture mark", "puncture wound", "track marks",
                               "tourniquet", "burnt spoon", "spoon", "cotton", "razor blades", "cut straws", "straws",
                               "rolled paper", "dollar bills", "roll dollar bill", "powder on mirror", "powder on table",
                               "powder on nose", "pipe", "tinfoil", "fentanyl patch", "pill", "tablet", 
                               "prescription bottles", "powder", "powdery substance", "white powdery substance", 
                               "crystal", "rock-like substance", "rock like substance", "plastic baggies", "baggies",
                               "pills", "crushed pills", "grinding device", "prescription bottle", "green leafy substance"]
druguseevidence_NOS = ["drug paraphernalia", "evidence of drug use"]
routeinjection = ["puncture mark", "puncture wound", "track marks", "tourniquet", "belt", "burnt spoon",
                         "spoon", "cotton", "uncapped syringe", "syringe cap", "needle cap", "syringe", "needle"]
    # _696_injection_evidence
indicationstracks = ["puncture mark", "puncture wound", "track marks"]
hasevidenceofinjectiontourni = ["tourniquet", "belt"]
hasevidenceofinjectioncooker = ["burnt spoon", "spoon"]
hasevidenceofinjectionneedle = ["uncapped syringe", "syringe cap", "syringe", "needle"]
_696_5_filters = ["cotton"]
_698_snort_sniff = ["razor blades", "cut straws", "straws", "rolled paper", "dollar bills", "powder on mirror",
                    "powder on table", "powder on nose"]
    # _699_snort_sniff_evidence
_699_1_straws = ["cut straws", "straws", "cut straw", "straw"]
_699_2_rolled_paper_or_dollar_bills = ["rolled paper", "dollar bills", "dollar bill"]
_699_3_razor_blades = ["razor blades"]
_699_4_powder_on_table_mirror = ["powder on mirror", "powder on table", "mirror with powder", "table with powder", 
                             "line of powder", "powder line"]
snortingpowdernose = ["powder on nose"]
hasroutesmoking = ["lighter", "pipes", "tinfoil", "vape pens", "e-cigarettes", "bong", "bowl", "copper", "chore boy", 
              "grinding device", "green leafy substance"]
    # _700_smoke_evidence 
smokingpipe = ["pipes", "torch", "torch lighter"]
smokingtinfoil = ["tinfoil", "foil"]
smokingvape =["vape pens", "e-cigarettes"]
smokingbongbowl = ["bong", "bowl"]
indicationsdrugsatscene = ["powder", "crystal", "rock-like substance", "plastic baggies", "baggies", "lottery ticket",
                             "residue", "white substance", "tan substance"]
    # _712_illict_drugs_evidence 
hasevidenceofillicitpowder = ["powder", "white powdery substance", "powdery substance", "residue"]
hasevidenceofillicittar = ["black tar", "tar"]
hasevidenceofillicitcrystal = ["crystal", "rock like substance", "crystalline substance"]
hasevidenceofillicitpackage = ["plastic baggies", "baggies", "lottery ticket", "folded lottery ticket"]
_185_relationship_status = ["girlfriend", "boyfriend", "partner", "significant other","intimate partner","husband","wife"]
    #_735_known_medical_conditions
medhx_COPD = ["copd", "chronic obstructive pulmonary disease"]
medhx_asthma = ["asthma"]
medhx_apnea = ["sleep apnea"]
medhx_heart = ["heart disease", "hypertension","high blood pressure","cardiovascular disease",
                        "coronary artery disease", "atherosclerotic cardiovascular disease","congestive heart failure",
              "atherosclerotic", "aortic", "atrial fibrilation", "ventricular", "pulmonary oedema", "embolism", 
              "tachycardia"]
medhx_obesity = ["obesity"]
#_735_6_history_of_major_injury
medhx_migraine = ["migraines"]
medhx_backpain = ["back pain","pain in back","lower back pain"]
medhx_hepc = ["hepatitis c", "hep c"]
medhx_hiv = ["hiv", "aids", "human immunodeficiency virus"]
medhx_otherpain = ["pain", "chronic pain", "acute pain"]
medhx_otherbreathing = ["emphysema", "lung cancer"]


# ### Converting the lists of unigram terms to tuples 

# In[7]:


forensic_center = (forensic_center_bigrams)
any_evidence_of_drug_use = (any_evidence_of_drug_use_bigrams)
other_substance_abuse = (other_substance_abuse_bigrams)
history_of_drug_use_terms = (history_of_drug_use_terms_bigrams)
history_of_alcohol_abuse = (history_of_alcohol_abuse_bigrams)
mental_health_condition = (mental_health_condition_bigrams)
traumatic_brain_injury = (traumatic_brain_injury_bigrams)
suicide_attempts = (suicide_attempts_bigrams)
suicide_ideation = (suicide_ideation_bigrams)
non_specific_evidence = (non_specific_evidence_bigrams)
evidence_of_injection = (evidence_of_injection_bigrams)
evidence_of_snorting_sniffing = (evidence_of_snorting_sniffing_bigrams)
evidence_of_smoking = (evidence_of_smoking_bigrams)
illicit_drug_evidence = (illicit_drug_evidence_bigrams)
relationship_status = (relationship_status_bigrams)
known_medical_conditions = (known_medical_conditions_bigrams)
hxheroin = (hxheroin)
hxrxopioid= (hxrxopioid)
hxanyopioid = (hxanyopioid)
hxfentanyl = (hxfentanyl)
hxcocaine = (hxcocaine)
hxmeth = (hxmeth)
hxbenzo = (hxbenzo)
hxcannabis = (hxcannabis)
hxunspecified=(hxunspecified)
cme_substanceabuseother=(cme_substanceabuseother)
cme_alcoholproblem = (cme_alcoholproblem)
cme_mentalhealthproblem = (cme_mentalhealthproblem)
cme_istraumaticbraininjuryhist = (cme_istraumaticbraininjuryhist)
cme_suicideattempthistory = (cme_suicideattempthistory)
cme_suicidethoughthistory= (cme_suicidethoughthistory)
indicationsdrugpara = (indicationsdrugpara)
druguseevidence_NOS = (druguseevidence_NOS)
routeinjection = (routeinjection)
indicationstracks = (indicationstracks)
hasevidenceofinjectiontourni = (hasevidenceofinjectiontourni)
hasevidenceofinjectioncooker = (hasevidenceofinjectioncooker)
hasevidenceofinjectionneedle = (hasevidenceofinjectionneedle)
snortingpowdernose = (snortingpowdernose)
hasroutesmoking = (hasroutesmoking)
smokingpipe = (smokingpipe)
smokingtinfoil = (smokingtinfoil)
smokingvape = (smokingvape)
smokingbongbowl = (smokingbongbowl)
indicationsdrugsatscene = (indicationsdrugsatscene)
hasevidenceofillicitpowder = (hasevidenceofillicitpowder)
hasevidenceofillicittar = (hasevidenceofillicittar)
hasevidenceofillicitcrystal = (hasevidenceofillicitcrystal)
hasevidenceofillicitpackage = (hasevidenceofillicitpackage)
#_185_relationship_status_ = (_185_relationship_status)
medhx_COPD = (medhx_COPD)
medhx_asthma = (medhx_asthma)
medhx_apnea = (medhx_apnea)
medhx_heart = (medhx_heart)
medhx_obesity = (medhx_obesity)
medhx_migraine = (medhx_migraine)
medhx_backpain = (medhx_backpain)
medhx_hepc = (medhx_hepc)
medhx_hiv = (medhx_hiv)
medhx_otherpain = (medhx_otherpain)
medhx_otherbreathing = (medhx_otherbreathing)


# In[ ]:


#### first, create a list of lists with all of the terms included in each variable and then create a dictionary 
#### after having created an list with the names of the variables


# In[8]:


list_of_vars = [forensic_center_bigrams, history_of_drug_use_terms_bigrams, other_substance_abuse_bigrams, 
                history_of_alcohol_abuse_bigrams, mental_health_condition_bigrams, traumatic_brain_injury_bigrams,
                suicide_attempts_bigrams, suicide_ideation_bigrams, any_evidence_of_drug_use_bigrams, 
                non_specific_evidence_bigrams, evidence_of_injection_bigrams, evidence_of_snorting_sniffing_bigrams,
                evidence_of_smoking_bigrams, illicit_drug_evidence_bigrams, relationship_status_bigrams,
                known_medical_conditions_bigrams, hxheroin, hxrxopioid, hxanyopioid, hxfentanyl, hxcocaine, hxmeth,
                hxbenzo, hxcannabis, hxunspecified, cme_substanceabuseother, cme_alcoholproblem, cme_mentalhealthproblem, 
                cme_istraumaticbraininjuryhist, cme_suicideattempthistory, cme_suicidethoughthistory, indicationsdrugpara,
                druguseevidence_NOS, routeinjection, indicationstracks, hasevidenceofinjectiontourni, 
                hasevidenceofinjectioncooker, hasevidenceofinjectionneedle, snortingpowdernose, hasroutesmoking,
                smokingpipe, smokingtinfoil, smokingvape, smokingbongbowl, indicationsdrugsatscene, 
                hasevidenceofillicitpowder, hasevidenceofillicittar, hasevidenceofillicitcrystal,
                hasevidenceofillicitpackage, #_185_relationship_status_,
                medhx_COPD, medhx_asthma, medhx_apnea,
                medhx_heart, medhx_obesity, medhx_migraine, medhx_backpain, medhx_hepc, medhx_hiv, medhx_otherpain,
                medhx_otherbreathing]     


# In[9]:


var_names = ["forensic_center_bigrams", "history_of_drug_use_terms_bigrams", "other_substance_abuse_bigrams", 
                "history_of_alcohol_abuse_bigrams", "mental_health_condition_bigrams", "traumatic_brain_injury_bigrams",
                "suicide_attempts_bigrams", "suicide_ideation_bigrams", "any_evidence_of_drug_use_bigrams", 
                "non_specific_evidence_bigrams", "evidence_of_injection_bigrams", "evidence_of_snorting_sniffing_bigrams",
                "evidence_of_smoking_bigrams", "illicit_drug_evidence_bigrams", "relationship_status_bigrams",
                "known_medical_conditions_bigrams", "hxheroin", "hxrxopioid", "hxanyopioid", "hxfentanyl", "hxcocaine",
                "hxmeth", "hxbenzo", "hxcannabis", "hxunspecified", "cme_substanceabuseother", "cme_alcoholproblem",
                "cme_mentalhealthproblem", "cme_istraumaticbraininjuryhist", "cme_suicideattempthistory", 
                "cme_suicidethoughthistory", "indicationsdrugpara", "druguseevidence_NOS", "routeinjection", 
                "indicationstracks", "hasevidenceofinjectiontourni", "hasevidenceofinjectioncooker", 
                "hasevidenceofinjectionneedle", "snortingpowdernose", "hasroutesmoking", "smokingpipe",
                "smokingtinfoil", "smokingvape", "smokingbongbowl", "indicationsdrugsatscene", "hasevidenceofillicitpowder",
                "hasevidenceofillicittar", "hasevidenceofillicitcrystal", "hasevidenceofillicitpackage", 
                "_185_relationship_status_", "medhx_COPD", "medhx_asthma", "medhx_apnea",
                "medhx_heart", "medhx_obesity", "medhx_migraine", "medhx_backpain", "medhx_hepc", "medhx_hiv",
                "medhx_otherpain", "medhx_otherbreathing"]


# In[39]:


# for inner_list in list_of_vars:
#     for element in inner_list:
#         print(inner_list[0])


# In[38]:


# list_b = copy.deepcopy(list_of_vars)


# In[10]:


result = dict(zip(var_names, list_of_vars))


# In[11]:


print(result['hxfentanyl'])


# ### Function measuring whether there's a match between any terms of a redcap variable list and a narrative summary

# In[12]:


def terms_match(rep, term_list):

    count = 0
    
    if any(word in rep for word in term_list):
        count = 1
    else:
        count = 0

    return count


# ### For loop that uses the terms_match function created above to search for matches of any of the terms linked to a given redcap variable and creates a new column for each variable in the original dataframe

# In[83]:


# result.keys()


# In[82]:


# for key, value in result.items():
#     narr_df.narr.apply()


# In[21]:


for key, value in result.items():
    narr_df[key] = narr_df['doc_clean'].apply(lambda x: terms_match(narr_df['doc_clean'], key)) 


# In[22]:


len(list_of_vars)


# In[14]:


for i in list_of_vars:
    print("variable for redcap:", i)
    for j in list_of_vars:
        print(j)
    for j in narr_df.narr:
        a = terms_match(rep= j, term_list = i)
        print(a)
        
        


# In[15]:


print(a)


# In[16]:


terms_match(rep = narr_df.doc_clean, term_list = hxheroin)


# In[17]:


a


# In[23]:


narr_df.columns


# In[24]:


narr_df.head(5)


# In[42]:


# creating tuples out of a list of lists
# for i in list_of_vars:
#     i = (* i,) 

# print(list_of_vars[:2])


# ### For loop that identifies specific terms found in autopsy narrative summaries and prints out the index of narrative summary

# In[160]:


# this code chunck works for a series of document/scripts and tuple of terms  
  # it throws an error when the narr_df.narr is NA

# count = 0
# term_list = history_of_drug_use_terms_bigrams_tuple # example of what a term list could be - also works with bigram terms tuple

# for j in range(len(narr_df.narr)):
#     for i in range(len(term_list)):
#         for match in re.finditer(term_list[i], str(narr_df.narr[j]), re.S):
#             count = count + 1
#             print(match)
#             print("narrative summary index :", [j])
#             print("total number of occurences of any listed terms so far:", count)  


# ## Creating the SUDORS Variables based on the count of occurrences of the listed bi-gram terms found in a given autopsy's narrative summary text

# In[25]:


term_list = forensic_center

narr_df["forensic_center_match"] = narr_df['doc_clean'].apply(lambda x: terms_match(x, term_list = term_list))


# In[28]:


term_list = other_substance_abuse

narr_df["other_substance_abuse"] = narr_df['doc_clean'].apply(lambda x: terms_match(x, term_list = term_list))


# In[27]:


term_list = history_of_drug_use_terms

narr_df["history_of_drug_use"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[29]:


term_list = history_of_alcohol_abuse

narr_df["history_of_alcohol_abuse"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[30]:


term_list = mental_health_condition

narr_df["mental_health_condition"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[31]:


term_list = traumatic_brain_injury

narr_df["traumatic_brain_injury"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[32]:


term_list = suicide_attempts

narr_df["suicide_attempts"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[33]:


narr_df.suicide_attempts.sum()


# In[34]:


term_list = suicide_ideation

narr_df["suicide_ideation"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[35]:


term_list = any_evidence_of_drug_use

narr_df["any_evidence_of_drug_use"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[36]:


term_list = non_specific_evidence

narr_df["non_specific_evidence"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[37]:


term_list = evidence_of_injection

narr_df["evidence_of_injection"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[38]:


term_list = evidence_of_snorting_sniffing

narr_df["evidence_of_snorting_sniffing"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[39]:


term_list = evidence_of_smoking

narr_df["evidence_of_smoking"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[40]:


term_list = illicit_drug_evidence

narr_df["illicit_drug_evidence"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[41]:


term_list = relationship_status

narr_df["relationship_status"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[42]:


term_list = known_medical_conditions

narr_df["known_medical_conditions"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[43]:


term_list = hxheroin

narr_df["hxheroin"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[44]:


term_list = hxrxopioid

narr_df["hxrxopioid"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[45]:


term_list = hxanyopioid

narr_df["hxanyopioid"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[46]:


term_list = hxfentanyl

narr_df["hxfentanyl"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[47]:


narr_df.hxfentanyl.sum()


# In[48]:


term_list = hxcocaine

narr_df["hxcocaine"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[49]:


term_list = hxmeth

narr_df["hxmeth"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[50]:


term_list = hxbenzo

narr_df["hxbenzo"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[51]:


term_list = hxcannabis

narr_df["hxcannabis"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[52]:


term_list = hxunspecified

narr_df["hxunspecified"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[53]:


term_list = snortingpowdernose

narr_df["cme_substanceabuseother"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[54]:


term_list = cme_alcoholproblem

narr_df["cme_alcoholproblem"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[55]:


term_list = cme_mentalhealthproblem

narr_df["cme_mentalhealthproblem"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[56]:


term_list = cme_istraumaticbraininjuryhist

narr_df["cme_istraumaticbraininjuryhist"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[57]:


term_list = cme_suicideattempthistory

narr_df["cme_suicideattempthistory"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[58]:


term_list = cme_suicidethoughthistory

narr_df["cme_suicidethoughthistory"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[59]:


term_list = indicationsdrugpara

narr_df["indicationsdrugpara"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[60]:


term_list = druguseevidence_NOS

narr_df["druguseevidence_NOS"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[61]:


term_list = routeinjection

narr_df["routeinjection"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[62]:


term_list = indicationstracks

narr_df["indicationstracks"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[63]:


term_list = hasevidenceofinjectiontourni

narr_df["hasevidenceofinjectiontourni"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[64]:


term_list = hasevidenceofinjectioncooker

narr_df["hasevidenceofinjectioncooker"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[65]:


term_list = hasevidenceofinjectionneedle

narr_df["hasevidenceofinjectionneedle"] = narr_df['doc_clean'].apply(lambda x: terms_match(x, term_list = term_list))


# In[66]:


narr_df.hasevidenceofinjectionneedle.sum()


# In[67]:


term_list = snortingpowdernose

narr_df["snortingpowdernose"] = narr_df['doc_clean'].apply(lambda x: terms_match(x, term_list = term_list))


# In[68]:


narr_df.snortingpowdernose.sum()


# In[69]:


term_list = hasroutesmoking

narr_df["hasroutesmoking"] = narr_df['doc_clean'].apply(lambda x: terms_match(x, term_list = term_list))


# In[70]:


narr_df.hasroutesmoking.sum()


# In[71]:


term_list = smokingpipe

narr_df["smokingpipe"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[72]:


term_list = smokingtinfoil

narr_df["smokingtinfoil"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[73]:


term_list = smokingvape

narr_df["smokingvape"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[74]:


term_list = smokingbongbowl

narr_df["smokingbongbowl"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[75]:


term_list = indicationsdrugsatscene

narr_df["indicationsdrugsatscene"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[76]:


term_list = hasevidenceofillicitpowder

narr_df["hasevidenceofillicitpowder"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[77]:


term_list = hasevidenceofillicittar

narr_df["hasevidenceofillicittar"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[78]:


term_list = hasevidenceofillicitcrystal

narr_df["hasevidenceofillicitcrystal"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[79]:


term_list = hasevidenceofillicitpackage

narr_df["hasevidenceofillicitpackage"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[80]:


term_list = medhx_COPD

narr_df["medhx_COPD"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[81]:


term_list = medhx_asthma

narr_df["medhx_asthma"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[82]:


term_list = medhx_apnea

narr_df["medhx_apnea"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[83]:


# term_list = medhx_heart

# narr_df["_711_evidence_illicit_drug"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[84]:


term_list = medhx_obesity

narr_df["medhx_obesity"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[85]:


term_list = medhx_migraine

narr_df["medhx_migraine"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[86]:


term_list = medhx_backpain

narr_df["medhx_backpain"] = narr_df['doc_clean'].apply(lambda x: terms_match(x, term_list = term_list))


# In[87]:


narr_df.medhx_backpain.sum()


# In[88]:


term_list = medhx_hepc

narr_df["medhx_hepc"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[89]:


narr_df.medhx_hepc.sum()


# In[90]:


term_list = medhx_hiv

narr_df["medhx_hiv"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[91]:


term_list = medhx_otherpain

narr_df["medhx_otherpain"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# In[92]:


narr_df.medhx_otherpain.sum()


# In[93]:


term_list = medhx_otherbreathing

narr_df["medhx_otherbreathing"] = narr_df['full_narr'].apply(lambda x: terms_match(x, term_list = term_list))


# ### Saving the dataframe with the added columns as a new feather file

# In[96]:


narr_df.to_feather('extracted_variables_from_SUDORS_narratives_2019-2022_11-22-22.feather')
# I got an error 'permission denied' when trying to save the feather file in the Code Files folder


# In[97]:


# saving the dataframe with bigram term counts as a spreadsheet
narr_df.to_excel("extracted_variables_from_SUDORS_narratives_2019-2022_11-22-22.xlsx")

