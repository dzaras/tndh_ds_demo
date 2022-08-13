#!/usr/bin/env python
# coding: utf-8

# # Extracting SUDORS Variables from Autopsies Using Uni-grams and Bi-grams

# In[1]:


import pandas as pd
import numpy as np
import os
import re

os.chdir("C:/Users/DC20B46/Documents")


# In[2]:


# read in the narr_df file where we have the scraped narratives from the autopsy reports
# narr_df = pd.read_csv (r'C:\Users\DC20B46\Documents\narr_df.csv') # this was the file used to develop this script
narr_df = pd.read_feather(r'T:\Data Science Demonstration Project\Code Files\narratives_sudors.feather') # data from '19-'20


# In[3]:


# print(narr_df.dtypes) # Print data types of columns - converting 'narr' from object to string wasn't necessary after all


# In[3]:


# create a separate dataframe only for the unigram term counts
narr_df_u = narr_df


# ## Lists of unigram terms associated with SUDORS variables

# In[4]:


# define unigram terms associated with variables
forensic_center = ["west tennessee regional forensic science center", "center for forensic medicine",
                   "hamilton county corensic center", "knox county regional forensic center",
                   "william l. jenkins forensic center, etsu"
                  ]

history_of_drug_use_terms = ["heroin", "opioid", "fentanyl", "cocaine", "crack", "meth", "methamphetamine", "xanax",
                             "benzo", "marijuana", "medication", "polysubstance"                             
                            ]

other_substance_abuse = ["heroin", "cocaine", "methamphetamine", "medication", "opioid", "marijuana", "polysubstance",
                         "substance"
                          ]

history_of_alcohol_abuse = [ "alcohol", "drinking", "drinker"]

mental_health_condition = ["depression", "dysthymia", "bipolar", "schizophrenia", "anxiety", 
                           "post-traumatic", "ptsd", "add", "adhd", "hyperactivity", 
                           "attention-deficit", "eating disorder", "obsessive-compulsive",
                           "ocd", "multiple personalities", "fetal alcohol syndrome", "dementia",
                           "down syndrome"]

traumatic_brain_injury = ["traumatic brain injury", "tbi"]

suicide_attempts = ["suicide attempt"]

suicide_ideation = ["ideation", "thoughts of suicide"]

any_evidence_of_drug_use = [ "paraphernalia", "syringe", "needle", "pipe", "puncture", "tourniquet", "spoon", "cotton",
                            "razor", "blades", "straws", "dollar", "bills", "powder", "mirror", "tinfoil", "fentanyl",
                            "pill", "tablet", "prescription", "powder", "crystal", "rock-like", "baggies", "pills"
                             ]

non_specific_evidence = [ "drug" , "paraphernalia"]
                         
evidence_of_injection = [ "puncture", "tourniquet", "belt", "spoon", "cotton", "syringe", "needle"
                        ]

evidence_of_snorting_sniffing = [ "razor", "blades", "straws", "rolled", "paper", "dollar", "bills",
                                 "powder", "mirror", "line"
                                ]                        

evidence_of_smoking = [ "lighter", "pipes", "tinfoil", "vape", "pens", "e-cigarettes", "bong", "bowl", "pipes", 
                       "tinfoil"  
                     ]

illicit_drug_evidence = ["powder", "crystal", "rock-like", "baggies", "powder", "powdery", "tar", "crystal", "baggies"
]

relationship_status = [ "girlfriend", "boyfriend", "partner", "husband", "wife" ]

known_medical_conditions = [ "copd", "chronic", "obstructive", "pulmonary", "asthma", "apnea", "disease",
                           "hypertension", "cardiovascular", "disease", "obesity", "migraines", "pain", "hep", "hepatitis",
                           "hiv", "aids", "pain", "emphysema", "cancer"
                          ]

# this next list is just to test the counter function
test_terms = [ "summary", "narrative" ]


# ### Converting the lists of unigram terms to tuples 

# In[5]:


test_terms_tuple = tuple(test_terms)
forensic_center_tuple = tuple(forensic_center) 
history_of_drug_use_terms_tuple = tuple(history_of_drug_use_terms)
other_substance_abuse_tuple = tuple(other_substance_abuse)                                       
any_evidence_of_drug_use_tuple = tuple(any_evidence_of_drug_use)
mental_health_condition_tuple = tuple(mental_health_condition)
traumatic_brain_injury_tuple = tuple(traumatic_brain_injury)
suicide_attempts_tuple = tuple(suicide_attempts)
suicide_ideation_tuple = tuple(suicide_ideation)
non_specific_evidence_tuple = tuple(non_specific_evidence)
history_of_alcohol_abuse_tuple = tuple(history_of_alcohol_abuse)
evidence_of_injection_tuple = tuple(evidence_of_injection)
evidence_of_snorting_sniffing_tuple = tuple(evidence_of_snorting_sniffing)
evidence_of_smoking_tuple = tuple(evidence_of_smoking)
illicit_drug_evidence_tuple = tuple(illicit_drug_evidence)
relationship_status_tuple = tuple(relationship_status)
known_medical_conditions_tuple = tuple(known_medical_conditions)


# ## Lists of bigram terms associated with SUDORS variables
# 
# ### Replaced the double quotation marks for all of the terms in these lists, otherwise the terms were not matched by the functions

# In[5]:


forensic_center_bigrams = ["west tennessee regional forensic science center", "center for forensic medicine",
                   "hamilton county corensic center", "knox county regional forensic center",
                   "william l. jenkins forensic center, etsu"
                  ]

history_of_drug_use_terms_bigrams = ["heroin abuse", "opiod abuse", "pain med abuse", "pain pill abuse", 
                             "opiod abuse", "fentanyl abuse", "cocaine abuse", "crack/cockaine abuse", 
                             "meth abuse", "methamphetamine abuse", "methamphetamine intoxication","meth use",
                             "methamphetamine abuse", "abuse xanax", "benzo abuse", "marijuana abuse", 
                             "history of drug abuse","history of drug use", "medication abuse", "polysubstance abuse"                             
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

evidence_of_smoking_bigrams = [ "lighter", "pipes", "tinfoil", "vape pens", "e-cigarettes", "bong", "bowl"
                                                    ]

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


# In[6]:


forensic_center_bigrams_tuple = tuple(forensic_center_bigrams)
any_evidence_of_drug_use_bigrams_tuple = tuple(any_evidence_of_drug_use_bigrams)
other_substance_abuse_bigrams_tuple = tuple(other_substance_abuse_bigrams)
history_of_drug_use_terms_bigrams_tuple = tuple(history_of_drug_use_terms_bigrams)
history_of_alcohol_abuse_bigrams_tuple = tuple(history_of_alcohol_abuse_bigrams)
mental_health_condition_bigrams_tuple = tuple(mental_health_condition_bigrams)
traumatic_brain_injury_bigrams_tuple = tuple(traumatic_brain_injury_bigrams)
suicide_attempts_bigrams_tuple = tuple(suicide_attempts_bigrams)
suicide_ideation_bigrams_tuple = tuple(suicide_ideation_bigrams)
non_specific_evidence_bigrams_tuple = tuple(non_specific_evidence_bigrams)
evidence_of_injection_bigrams_tuple = tuple(evidence_of_injection_bigrams)
evidence_of_snorting_sniffing_bigrams_tuple = tuple(evidence_of_snorting_sniffing_bigrams)
evidence_of_smoking_bigrams_tuple = tuple(evidence_of_smoking_bigrams)
illicit_drug_evidence_bigrams_tuple = tuple(illicit_drug_evidence_bigrams)
relationship_status_bigrams_tuple = tuple(relationship_status_bigrams)
known_medical_conditions_bigrams_tuple = tuple(known_medical_conditions_bigrams)


# ### For loop that identifies specific terms found in autopsy narrative summaries and prints out the index of narrative summary

# In[9]:


# this code chunck works for a series of document/scripts and tuple of terms  
  # it throws an error when the narr_df.narr is NA

count = 0
term_list = history_of_alcohol_abuse_tuple # example of what a term list could be - also works with bigram terms tuple

for j in range(len(narr_df.narr)):
    for i in range(len(term_list)):
        for match in re.finditer(term_list[i], str(narr_df.narr[j]), re.S):
            count = count + 1
            print(match)
            print("narrative summary index :", [j])
            print("total number of occurences of any listed terms so far:", count)  


# ## Creating a function for both unigram and bigram lists of terms associated with each one of the SUDORS variables

# In[6]:


def terms_count(rep, term_list):

    count = 0

    for i in range(len(term_list)):
        for match in re.finditer(term_list[i], str(rep), re.S):
            count = count + 1

    return count


# In[11]:


# old version of function for a specific terms list
# narr_df["history_of_drug_use_terms_count"] = narr_df["narr"].apply(history_of_drug_use_terms_count)


# In[12]:


# first, define the term list we want to use the function with
term_list = history_of_drug_use_terms_tuple

narr_df["history_of_drug_use_terms_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[13]:


print(narr_df.history_of_drug_use_terms_count)


# In[14]:


# bigram test terms to check the terms_count function 
test_terms_bigram = ["narrative summary", "powdery substance"]
test_terms_bigram_tuple = tuple(test_terms_bigram)


# In[15]:


# in this case, I use the terms_count function with a bi-gram terms list
term_list = test_terms_bigram_tuple

narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))
# when using these test terms with the earlier version of the dataset that contained 2020 and 2021 narratives, 
# I had noticed that the term 'powdery substance' appeared in the narrative 
# summary text with index '1'. Based on those results, we know that the function works properly


# ## Creating the SUDORS Variables based on the count of occurrences of the listed bi-gram terms found in a given autopsy's narrative summary text 

# In[8]:


term_list = forensic_center_bigrams_tuple

narr_df["forensic_center_bigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[9]:


term_list = history_of_drug_use_terms_bigrams_tuple

narr_df["history_of_drug_use_bigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[10]:


term_list = illicit_drug_evidence_bigrams_tuple

narr_df["illicit_drug_evidence_bigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[11]:


term_list = other_substance_abuse_bigrams_tuple

narr_df["other_substance_abuse_bigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[12]:


term_list = history_of_alcohol_abuse_bigrams_tuple

narr_df["history_of_alcohol_abuse_bigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[13]:


term_list = mental_health_condition_bigrams_tuple

narr_df["mental_health_condition_bigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[14]:


term_list = traumatic_brain_injury_bigrams_tuple

narr_df["traumatic_brain_injury_bigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[15]:


term_list = suicide_attempts_bigrams_tuple

narr_df["suicide_attempts_bigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[16]:


term_list = suicide_ideation_bigrams_tuple

narr_df["suicide_ideation_bigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[17]:


term_list = any_evidence_of_drug_use_bigrams_tuple

narr_df["any_evidence_of_drug_use_bigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[18]:


term_list = non_specific_evidence_bigrams_tuple

narr_df["non_specific_evidence_bigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[19]:


term_list = evidence_of_injection_bigrams_tuple

narr_df["evidence_of_injection_bigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[20]:


term_list = evidence_of_snorting_sniffing_bigrams_tuple

narr_df["evidence_of_snorting_sniffing_bigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[21]:


term_list = evidence_of_smoking_bigrams_tuple

narr_df["evidence_of_smoking_bigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[22]:


term_list = relationship_status_bigrams_tuple

narr_df["relationship_status_bigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[23]:


term_list = known_medical_conditions_bigrams_tuple

narr_df["known_medical_conditions_bigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# ## SUDORS Variables based on the count of occurrences of the listed uni-gram terms found in a given autopsy's narrative summary text

# In[7]:


term_list = forensic_center_tuple

narr_df_u["forensic_center_unigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[8]:


term_list = history_of_drug_use_terms_tuple

narr_df_u["history_of_drug_use_unigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[9]:


term_list = illicit_drug_evidence_tuple

narr_df_u["illicit_drug_evidence_unigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[10]:


term_list = other_substance_abuse_tuple

narr_df_u["other_substance_abuse_unigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[11]:


term_list = history_of_alcohol_abuse_tuple

narr_df_u["history_of_alcohol_abuse_unigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[12]:


term_list = mental_health_condition_tuple

narr_df_u["mental_health_condition_unigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[13]:


term_list = traumatic_brain_injury_tuple

narr_df_u["traumatic_brain_injury_unigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[14]:


term_list = suicide_attempts_tuple

narr_df_u["suicide_attempts_unigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[15]:


term_list = suicide_ideation_tuple

narr_df["suicide_ideation_unigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[16]:


term_list = any_evidence_of_drug_use_tuple

narr_df_u["any_evidence_of_drug_use_unigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[17]:


term_list = non_specific_evidence_tuple

narr_df_u["non_specific_evidence_unigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[18]:


term_list = evidence_of_injection_tuple

narr_df_u["evidence_of_injection_unigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[19]:


term_list = evidence_of_snorting_sniffing_tuple

narr_df_u["evidence_of_snorting_sniffing_unigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[20]:


term_list = evidence_of_smoking_tuple

narr_df_u["evidence_of_smoking_unigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[21]:


term_list = relationship_status_tuple

narr_df_u["relationship_status_unigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[22]:


term_list = known_medical_conditions_tuple

narr_df_u["known_medical_conditions_unigrams_count"] = narr_df['narr'].apply(lambda x: terms_count(x, term_list = term_list))


# In[23]:


print(narr_df_u.columns)


# ### Saving the dataframe with the added columns as a new feather file

# In[24]:


narratives_sudors_extracted_variables_bigrams = narr_df


# In[25]:


narratives_sudors_extracted_variables_bigrams.to_feather('narratives_sudors_extracted_variables_bigrams.feather')
# I got an error 'permission denied' when trying to save the feather file in the Code Files folder


# In[26]:


# saving the dataframe with bigram term counts as a spreadsheet
narr_df.to_excel("narratives_sudors_extracted_variables_bigrams.xlsx")


# In[25]:


# for the unigrams dataframe
narratives_sudors_extracted_variables_unigrams = narr_df_u


# In[26]:


narratives_sudors_extracted_variables_unigrams.to_feather('narratives_sudors_extracted_variables_unigrams.feather')


# In[24]:


# saving the unigram dataframe with unigram counts as a spreadsheet
narr_df_u.to_excel("narratives_sudors_extracted_variables_unigrams.xlsx")

