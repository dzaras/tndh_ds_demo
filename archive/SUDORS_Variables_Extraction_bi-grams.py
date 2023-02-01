#!/usr/bin/env python
# coding: utf-8

# # Extracting SUDORS Variables from Autopsies

# In[1]:


import pandas as pd
import numpy as np
import os
import re
from collections import Counter

# os.chdir("C:/Users/DC20B46/Documents")


# In[2]:


# read in the narr_df file where we have the scraped narratives from the autopsy reports
narr_df = pd.read_csv (r'C:\Users\DC20B46\Documents\narr_df.csv')


# In[3]:


narr_df.head()


# In[4]:


# define terms associated with variables
history_of_drug_use_terms = ["heroin abuse", "opiod abuse", "pain med abuse", "pain pill abuse", 
                             "opiod abuse", "fentanyl abuse", "cocaine abuse", "crack/cockaine abuse", 
                             "meth abuse", "methamphetamine abuse", "methamphetamine intoxication","meth use",
                             "methamphetamine abuse", "abuse xanax", "benzo abuse", "marijuana abuse", 
                             "history of drug abuse","history of drug use", "medication abuse", "polysubstance abuse"                             
                            ]
# I added the term 'methamphetamine intoxication' in the history_of_drug_abuse because I saw it in narr_df.narr[3]
other_substance_abuse = ["heroin abuse”, “cocaine abuse”, “methamphetamine abuse”, “history of drug abuse",
                         "medication abuse", "opioid abuse”, “pain med abuse”, “pain pill abuse”, “marijuana abuse",
                         "polysubstance abuse”, “substance abuse"
                          ]

history_of_alcohol_abuse = [ "alcohol abuse”, “heavy drinking”, “heavy drinker”, “alcohol use"]

any_evidence_of_drug_use = [ "drug paraphernalia”, “uncapped syringe”, “syringe cap”, “needle cap”, “syringe",
                            "needle”, “glass pipe”, “puncture mark”, “puncture wound”, “track marks”, “tourniquet",
                            "burnt spoon”, “spoon”, “cotton”, “razor blades”, “cut straws”, “straws”, “rolled paper",
                            "dollar bills”, “powder on mirror”, “powder on table”, “powder on nose”, “pipe”, “tinfoil",
                            "fentanyl patch”, “pill”, “tablet”, “prescription bottles”, “powder”, “powdery substance",
                            "white powdery substance”, “crystal”, “rock-like substance”, “plastic baggies”, “baggies",
                            "pills"
                             ]

non_specific_evidence = [ "drug paraphernalia", "evidence of drug use"]
                         
evidence_of_injection = [ "puncture mark”, “puncture wound”, “track marks”, “tourniquet”, “belt”, “burnt spoon",
                         "spoon”, “cotton”, “uncapped syringe”, “syringe cap”, “needle cap”, “syringe”, “needle",
                         "puncture mark”, “puncture wound”, “track marks”, “tourniquet”, “belt”, “burnt spoon”, “spoon",
                         "uncapped syringe”, “syringe cap”, “syringe”, “needle", "cotton"
                        ]

evidence_of_snorting_sniffing = [ "razor blades", "cut straws”, “straws”, “rolled paper”, “dollar bills", 
                                 "powder on mirror", "powder on table", "powder on nose”, “cut straws”, “straws",
                                 "rolled paper”, “dollar bills”, “razor blades”, “powder on mirror”, “powder on table",
                                 "mirror with powder”, “table with powder”, “line of powder”, “powder line", 
                                 "powder on nose"
                                ]                        

evidence_of_smoking = [ "lighter", "pipes”, “tinfoil”, “vape pens”, “e-cigarettes”, “bong”, “bowl”, “pipes”, “tinfoil",
                       "vape pens”, “e-cigarettes”, “bong”, “bowl"    
                     ]

illicit_drug_evidence = [ "powder”, “crystal”, “rock-like substance”, “plastic baggies”, “baggies”, “powder", 
                         "white powdery substance", "powdery substance”, “black tar”, “tar”, “crystal", 
                         "rock like substance”, “plastic baggies”, “baggies"
                        ]

relationship_status = [ "girlfriend”, “boyfriend”, ”partner”, “significant other" ]

know_medical_conditions = [ "COPD”, “chronic obstructive pulmonary disease”, “asthma”, “sleep apnea”, “heart disease",
                           "hypertension”, “cardiovascular disease”, “obesity”, “migraines”, “back pain”, “Hep C",
                           "Hepatitis C”, “HIV”, “AIDS”, “Pain”, “Emphysema”, “lung cancer"
                          ]

# this next list is just to test the counter function
test_terms = [ "summary", "narrative" ]


# In[5]:


narr_df.narr[3]


# In[6]:


testSTR = narr_df.narr[3]

print(len(re.findall(r"\bmedical examiner\b", testSTR)))
print(len(re.findall(r"\bdrug toxicity\b", testSTR)))

num_occurrences = (len(re.findall("\bmedical examiner\b", testSTR)))
print("number of occurences:", num_occurrences)


# In[148]:




print(len(re.findall(r"\bdrug\b", report)))


# In[12]:


# report = narr_df.narr[3]

def history_of_drug_use_terms_count(self):

    a = len(re.findall(r"\bheroin abuse\b", report))
    b = len(re.findall(r"\bopiod abuse\b", report))
    c = len(re.findall(r"\bpain med abuse\b", report))
    d = len(re.findall(r"\bpain pill abuse\b", report))
    e = len(re.findall(r"\bopiod abuse\b", report))
    f = len(re.findall(r"\bfentanyl abuse\b", report))
    g = len(re.findall(r"\bcocaine abuse\b", report))
    h = len(re.findall(r"\bcrack/cocaine abuse\b", report))
    i = len(re.findall(r"\bopiod abuse\b", report))
    j = len(re.findall(r"\bfentanyl abuse\b", report))
    k = len(re.findall(r"\bmeth abuse\b", report))
    l = len(re.findall(r"\bmethamphetamine abuse\b", report))
    m = len(re.findall(r"\bmethamphetamine intoxication\b", report))
    n = len(re.findall(r"\bemth use\b", report))
    o = len(re.findall(r"\bxanax abuse\b", report))
    p = len(re.findall(r"\bbenzo abuse\b", report))
    q = len(re.findall(r"\bpolysubstance abuse\b", report))
    r = len(re.findall(r"\bmarijuana abuse\b", report))
    s = len(re.findall(r"\bhistory of drug abuse\b", report))
    t = len(re.findall(r"\bhistory of drug use\b", report))
    u = len(re.findall(r"\bmedication abuse\b", report))



    total_num_occurrences = a + b + c + d + e + f + g + h + i + j + k + l + m + n + o + p + q + r + s + t + u
    # print("number of occurences:", total_num_occurrences)
    
    return total_num_occurrences


# In[16]:


# narr_df.narr = (str(narr_df.narr))
narr_df.narr[1].apply(history_of_drug_use_terms_count())


# In[17]:


# applying the function 
# narr_df['drug_use_terms_count'] = narr_df.apply(lambda row : history_of_drug_use_terms_count(row['narr']), axis = 1)
narr_df['drug_use_terms_count'] = narr_df['narr'].apply(history_of_drug_use_terms_count())


# In[151]:


print(narr_df['drug_use_terms_count'].describe())


# In[168]:


testSTR = narr_df.narr[3]
result = (re.search("\bsubstance\b", testSTR))
print(result)


# In[90]:


# function to count the number of occurrences of a word in the given string

def countOccurrences(rep, word):
     
    # search for pattern in a
    count = 0
    #for i in range(0, len(word)):
    for i in (word):  

         count = count + len(re.findall(word, rep))
            
    return count      


# In[37]:


word = any_evidence_of_drug_use
rep = narr_df.narr[1]

def binary_dict_check(rep, word):

    for x in (word):
        if any(x in rep for x in word):
            print('True')
       


# In[112]:


# test run with the test_terms
# narr_df["test_terms_count"] = narr_df["narr"].apply(countOccurrences, word = test_terms)
# b = narr_df["narr"].apply(countOccurrences, word = "drug")


# In[124]:


# print(narr_df.test_terms_count)


# ## Here I go through the narratives in the 'narr' column to check if there are matches for the terms associated with one of the SUDORS variables

# In[107]:


narr_df["history_of_drug_use_terms_count"] = narr_df["narr"].apply(history_of_drug_use_terms_count)


# In[88]:


narr_df["drug_use_terms_count"] = narr_df["narr"].str.split(" ").apply(countOccurrences, word = history_of_drug_use_terms)


# In[31]:


narr_df.drug_use_terms_count.sum()


# In[57]:


narr_df["drug_use_terms_count"] = narr_df["interp"].str.split(" ").apply(countOccurrences, word = history_of_drug_use_terms)


# In[33]:


narr_df.other_substance_abuse_terms_count.sum()


# In[34]:


narr_df["history_of_alcohol_abuse_count"] = narr_df["narr"].str.split(" ").apply(countOccurrences, word = history_of_alcohol_abuse)


# In[35]:


narr_df.history_of_alcohol_abuse_count.sum()


# In[36]:


narr_df["any_evidence_of_drug_use_count"] = narr_df["narr"].str.split(" ").apply(countOccurrences, word = any_evidence_of_drug_use)


# In[38]:


narr_df.history_of_alcohol_abuse_count.sum()


# In[ ]:


narr_df["non_specific_evidence_count"] = narr_df["narr"].str.split(" ").apply(countOccurrences, word = non_specific_evidence)


# In[39]:


narr_df.history_of_alcohol_abuse_count.sum()


# In[41]:


narr_df["evidence_of_injection_count"] = narr_df["narr"].str.split(" ").apply(countOccurrences, word = evidence_of_injection)


# In[42]:


narr_df.evidence_of_injection_count.sum()


# In[89]:


narr_df["evidence_of_snorting_sniffing_count"] = narr_df["narr"].str.split(" ").apply(countOccurrences, word = evidence_of_snorting_sniffing)


# In[44]:


narr_df.evidence_of_snorting_sniffing_count.sum()


# In[45]:


narr_df["evidence_of_smoking_count"] = narr_df["narr"].str.split(" ").apply(countOccurrences, word = evidence_of_smoking)


# In[46]:


narr_df.evidence_of_smoking_count.sum()


# In[47]:


narr_df["illicit_drug_evidence_count"] = narr_df["narr"].str.split(" ").apply(countOccurrences, word = illicit_drug_evidence)


# In[48]:


narr_df.illicit_drug_evidence_count.sum()


# In[49]:


narr_df["relationship_status_count"] = narr_df["narr"].str.split(" ").apply(countOccurrences, word = relationship_status)


# In[50]:


narr_df.relationship_status_count.sum()


# In[51]:


narr_df["know_medical_conditions_count"] = narr_df["narr"].str.split(" ").apply(countOccurrences, word = know_medical_conditions)


# In[52]:


narr_df.know_medical_conditions_count.sum()


# In[117]:


# Looking at a few individual documents
str = narr_df.narr[4]
word = history_of_drug_use_terms 
print(countOccurrences(str, word))


# In[53]:


str = narr_df.narr[10]
word = any_evidence_of_drug_use
print(countOccurrences(str, word))


# In[60]:


# saving the new dataframe with the added columns
narr_df.to_csv("narr_df_2.csv")

