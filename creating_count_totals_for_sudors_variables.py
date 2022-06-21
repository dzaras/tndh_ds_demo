#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import os
import re

os.chdir("C:/Users/DC20B46/Documents")


# In[48]:


# importing feather file with bigram terms counts
narr_df = pd.read_feather(r'C:/Users/DC20B46/Documents/narratives_sudors_extracted_variables_bigrams.feather') # data from '19-'20


# In[49]:


print(narr_df.columns)


# In[50]:


narr_df.history_of_drug_use_bigrams_count.sum()


# In[57]:


# print(" \nCount total NaN at each column in the DataFrame : \n\n",
#      narr_df.isnull().sum())


# In[51]:


print(len(narr_df))


# In[54]:


round(narr_df.any_evidence_of_drug_use_bigrams_count.mean(), 2)


# In[83]:


narr_df_totals = pd.DataFrame()
narr_df_totals["total_count"] = ""
print(narr_df_totals)


# In[85]:


narr_df_totals.total_count = narr_df[['forensic_center_bigrams_count','history_of_drug_use_bigrams_count',
                              'illicit_drug_evidence_bigrams_count','other_substance_abuse_bigrams_count', 
                              'history_of_alcohol_abuse_bigrams_count', 'mental_health_condition_bigrams_count',
                              'traumatic_brain_injury_bigrams_count','suicide_attempts_bigrams_count',
                              'suicide_ideation_bigrams_count',
                              'any_evidence_of_drug_use_bigrams_count', 'non_specific_evidence_bigrams_count',
                              'evidence_of_injection_bigrams_count', 'evidence_of_snorting_sniffing_bigrams_count',
                              'evidence_of_smoking_bigrams_count', 'relationship_status_bigrams_count',
                              'known_medical_conditions_bigrams_count'
                             ]].apply(sum)
print(narr_df_totals)


# In[86]:


narr_df_totals.to_csv("narr_df_bigrams_totals.csv")


# ## for the unigrams counts dataframe

# In[3]:


narr_df_u = pd.read_feather(r'C:/Users/DC20B46/Documents/narratives_sudors_extracted_variables_unigrams.feather') # data from '19-'20


# In[4]:


print(narr_df_u.columns)


# In[5]:


narr_df_u_totals = pd.DataFrame()
narr_df_u_totals["total_count"] = ""
print(narr_df_u_totals)


# In[7]:


narr_df_u_totals.total_count = narr_df_u[['forensic_center_unigrams_count', 'history_of_drug_use_unigrams_count',
       'illicit_drug_evidence_unigrams_count',
       'other_substance_abuse_unigrams_count',
       'history_of_alcohol_abuse_unigrams_count',
       'mental_health_condition_unigrams_count',
       'traumatic_brain_injury_unigrams_count',
       'suicide_attempts_unigrams_count', 'suicide_ideation_unigrams_count',
       'any_evidence_of_drug_use_unigrams_count',
       'non_specific_evidence_unigrams_count',
       'evidence_of_injection_unigrams_count',
       'evidence_of_snorting_sniffing_unigrams_count',
       'evidence_of_smoking_unigrams_count',
       'relationship_status_unigrams_count',
       'known_medical_conditions_unigrams_count'
                             ]].apply(sum)
print(narr_df_u_totals)


# In[8]:


narr_df_u_totals.to_csv("narr_df_unigrams_totals.csv")

