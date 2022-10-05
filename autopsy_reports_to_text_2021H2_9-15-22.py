#!/usr/bin/env python
# coding: utf-8

# # 2021H2 Autopsy Reports to Text

# #### The following script is for 2021 SUDORS (overdose) autopsies uploaded on the 2021 H2 folder by 9/15/22

# In[1]:


import os
import re  # for working with regular expressions
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

# path with autopsies    
path = 'Z:/2021 H2'

### generate file with DID-forensic center map (run once)
file_paths = list_files(path)
len(file_paths)


# In[2]:


os.getcwd()


# In[3]:


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


# In[6]:


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

a.to_feather('C:/Users/DC20B46/Documents/autopsies_original_sudors_2021H2.feather')

a.head()


# In[5]:


# saving the dataframe with the 2021H1 SUDORS autopsies as a spreadsheet
a.to_excel("autopsies_original_sudors2021H2.xlsx")

