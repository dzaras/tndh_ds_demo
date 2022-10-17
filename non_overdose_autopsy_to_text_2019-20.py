#!/usr/bin/env python
# coding: utf-8

# # Non-overdose Autopsy Reports to Text

# ## First, the autopsies from 2019

# In[1]:


import os
import re
from pdfminer.high_level import extract_text
import pandas as pd 

# list all autopsy files in subfolders
def list_files(dir):
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            if 'autopsy' in name.lower() and 'roi' not in name.lower():
                r.append(os.path.join(root, name))
            elif re.match(string=name.lower(), pattern='[a-z]+\.[a-z]+'):
                r.append(os.path.join(root, name))
    return r

# path with autopsies from 2019   
path = 'Z:/APHA Data Science Grant/2019'

### generate file with DID-forensic center map (run once)
file_paths = list_files(path)
len(file_paths)


# In[3]:


### import autopsies from specific forensic center
autopsies = dict()
for i, file_path in enumerate(file_paths):
    if i % 1000 == 0:                # this is included to show progress
        print(i)
        
    try:
        new_doc = extract_text(file_path)
        autopsies.update({file_path: new_doc})
    except:
        print(f'{file_path} cannot be opened.')

len(autopsies.keys())


# In[33]:


a=pd.DataFrame(autopsies.values(), index = autopsies.keys(), 
               columns = ['doc']).reset_index().rename(columns={'index':'File_Path'})
a['DID'] = a['File_Path'].str.extract('([0-9]+)_')
a['full_name'] = a['File_Path'].str.lower().str.extract('([a-z\-\s\']+(?:\.)[a-z\-\s\']+)')
a['first_name'] = a.apply(lambda x: re.sub('\..*$', '', x['full_name']) if pd.notna(x['DID'])
                          else re.sub('^.*\.', '', x['full_name']), axis = 1)
a['last_name'] = a.apply(lambda x: re.sub('\..*$', '', x['full_name']) if pd.isna(x['DID'])
                          else re.sub('^.*\.', '', x['full_name']), axis = 1)
a['Year'] = a['DID'].str[:4] # extract the first four digits of DID to identify year 

a.drop(columns='full_name', inplace = True)

a.head()


# ## Autopsies from 2020

# In[6]:


# path with autopsies from 2020
path = 'Z:/APHA Data Science Grant/2020'

### generate file with DID-forensic center map (run once)
file_paths = list_files(path)
len(file_paths)


# In[7]:


### import autopsies from specific forensic center
autopsies = dict()
for i, file_path in enumerate(file_paths):
    if i % 1000 == 0:
        print(i)
        
    try:
        new_doc = extract_text(file_path)
        autopsies.update({file_path: new_doc})
    except:
        print(f'{file_path} cannot be opened.')

len(autopsies.keys())


# In[8]:


b=pd.DataFrame(autopsies.values(), index = autopsies.keys(), 
               columns = ['doc']).reset_index().rename(columns={'index':'File_Path'})
b['DID'] = b['File_Path'].str.extract('([0-9]+)_')
b['full_name'] = b['File_Path'].str.lower().str.extract('([a-z\-\s\']+(?:\.)[a-z\-\s\']+)')
b['first_name'] = b.apply(lambda x: re.sub('\..*$', '', x['full_name']) if pd.notna(x['DID'])
                          else re.sub('^.*\.', '', x['full_name']), axis = 1)
b['last_name'] = b.apply(lambda x: re.sub('\..*$', '', x['full_name']) if pd.isna(x['DID'])
                          else re.sub('^.*\.', '', x['full_name']), axis = 1)
b['Year'] = a['DID'].str[:4] # extract the first four digits of DID to identify year 

b.drop(columns='full_name', inplace = True)

# a.to_feather('autopsies_original_non_overdose_2019.feather')

b.head()


# In[11]:


dfs = [a, b]
c = pd.concat(dfs)
display(c)


# In[18]:


c_r = c.reset_index(drop=True)
print(c_r)


# In[20]:


c_r.to_feather('C:/Users/DC20B46/Documents/autopsies_original_non_overdose_2019_20.feather')


# In[21]:


# saving the dataframe with bigram term counts as a spreadsheet
c_r.to_excel("autopsies_original_non_overdose_2019_20.xlsx")

