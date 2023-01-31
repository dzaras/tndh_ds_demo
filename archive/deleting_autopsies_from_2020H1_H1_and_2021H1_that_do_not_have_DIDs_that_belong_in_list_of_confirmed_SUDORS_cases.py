#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import pandas as pd
import numpy as np
import re


# ### Import the dataset created after converting the pdfs from the 2020H1,H2 and 2021H1 folders to text (after I had downloaded those folders to my local drive)

# In[3]:


narr_df = pd.read_excel(r'C:\Users\DC20B46\Documents\autopsies_original_sudors_2020H1_local.xlsx')


# In[4]:


narr_df.columns


# In[13]:


narr_df.shape


# In[21]:


narr_df.DID = narr_df.DID.astype(str)


# ### We want to delete the autopsies that appear to have a DID that's not included in the list of DIDs of confirmed SUDORS cases

# In[15]:


df2 = pd.read_excel(r'C:\Users\DC20B46\Documents\DIDs_in_Jessicas_list_but_not_Dimitris_2020-21.xlsx')


# In[18]:


df2.dtypes


# In[17]:


df2.DID = df2.DID.astype(str)


# In[25]:


#!pip install ipython-sql


# In[26]:


dids_to_keep = df2.DID.tolist()


# In[30]:


df_new = narr_df[narr_df.DID.isin(dids_to_keep)]


# In[31]:


df_new.shape


# In[34]:


df_new.drop(df_new.columns[0], axis=1, inplace=True)


# In[35]:


df_new.head()


# In[38]:


df_new.Year.value_counts()


# In[40]:


df_new.to_excel('C:/Users/DC20B46/Documents/autopsies_sudors_clean_2020-21_local.xlsx')

