#!/usr/bin/env python
# coding: utf-8

# # Concatenating the Overdose and Non-SUDORS Autopsy Narrative Summaries from 2019 and 2020

# ## Import datasets of overdose and non-overdose autopsy narrative summaries and combine them into a new dataset (6/8/22)

# In[2]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re


# In[118]:


non_od_df = pd.read_feather(r'C:\Users\DC20B46\Documents\narratives_non_overdose_2019_20.feather')


# In[119]:


non_od_df.shape


# In[121]:


non_od_df.columns


# ### Find and delete non-od narrative summaries that already appear in the sudors narrative summaries

# In[122]:


df3 = pd.read_csv(r'C:\Users\DC20B46\Downloads\nonOD_possible_SUDORS_cases.csv')


# In[123]:


df3.dtypes


# In[124]:


df3.DID = df3.DID.astype(str)


# In[125]:


dids_to_delete = df3.DID.tolist()


# In[126]:


print(non_od_df.DID.loc[non_od_df['DID'] == '2019006910'])


# In[127]:


len(dids_to_delete)  # we have 7390 rows in the dataframe of non-od narrative summaries, so we want to end up with 7288


# In[128]:


non_od_df2 = non_od_df.drop(non_od_df.index[non_od_df['DID'].isin(dids_to_delete)])


# In[129]:


len(non_od_df2)


# In[130]:


### create new 'OD' column to distinguish between od and non-od narrative summaries in the new combined dataset 
non_od_df2.insert(11, 'od', 0)


# In[131]:


od_df = pd.read_feather(r'C:\Users\DC20B46\Documents\narratives_sudors.feather')


# In[132]:


od_df.shape


# In[133]:


### create new 'OD' column to distinguish between od and non-od narrative summaries in the new combined dataset 
od_df.insert(11, 'od', 1)


# In[134]:


# concatenate the two dataframes
dfs = [non_od_df2, od_df]
c = pd.concat(dfs)
# display(c)


# In[135]:


c_r = c.reset_index(drop=True)
print(c_r)


# In[136]:


c_r.groupby('forensic_center').agg({'DID': 'nunique',
                                        'has_narr': 'sum',
                                        'has_interp': 'sum',
                                        'has_circ': 'sum',
                                        'od': 'sum'})


# In[1]:


c_r.groupby('year').agg({'DID': 'nunique',
                          'od' : 'sum',
                        'forensic_center':'nunique'})


# In[138]:


c_r.od.value_counts()


# In[55]:


# c_r.dtypes


# In[139]:


c_r['year'] = c_r['year'].astype(str)  # I did this because I was getting an error when trying to save c_r as a feather file


# In[142]:


c_r.to_feather('C:/Users/DC20B46/Documents/narr_od_nonod_2019_20.feather')


# In[143]:


c_r.to_excel('C:/Users/DC20B46/Documents/narr_od_nonod_2019_20.xlsx')

