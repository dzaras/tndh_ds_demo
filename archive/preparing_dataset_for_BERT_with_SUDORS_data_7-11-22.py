#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import re
import nltk
import random
from sklearn.utils import shuffle
import os
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

os.chdir('C:/Users/DC20B46/Documents/')


# In[3]:


narr_df = pd.read_feather('narratives_all_2019-2021h1.feather')


# In[6]:


narr_df.columns


# In[11]:


# Remove a few columns to match the dataframe column names of the dataframe Leigh Anne used in her analysis
narr_df = narr_df.drop(['forensic_center','doc_clean', 'narr', 'interp', 'circ', 'has_narr','has_interp', 'has_circ', 'full_narr_len'], axis = 1)


# In[12]:


narr_df.head()


# In[14]:


narr_df.to_csv('C:/Users/DC20B46/Documents/narratives_all_2019-21h1_for_bert.csv')


# In[10]:


narr_df.full_narr[2]

