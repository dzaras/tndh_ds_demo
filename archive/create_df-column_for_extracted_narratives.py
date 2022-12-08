#!/usr/bin/env python
# coding: utf-8

# In[19]:


import os
from pdfminer.high_level import extract_text
import pandas as pd
import numpy as np
import re
import pyarrow


# In[1]:


#!pip install pyarrow # not necessary anymore


# In[20]:


info_file_path = 'T:/Data Science Demonstration Project/Code Files/autopsies.feather'

readframe = pd.read_feather(info_file_path)


# In[22]:


print(readframe.head)


# In[23]:


readframe.doc[1]


# In[37]:


# create empty dataframe column to populate with the extracted narratives
readframe['narr'] = ''


# In[41]:


readframe.head()


# In[56]:


string_pattern = r'^.*(?=external examination'

out  = re.compile(r'^.*(?=external examination').match(readframe.doc[1])
if out :
    print(out)


# In[42]:


for i in readframe.doc:
    
    narr_re = re.compile(r'^.*(?=external examination)')
    if narr_re :
        readframe.narr = narr_re


# In[43]:


print(readframe.narr)

