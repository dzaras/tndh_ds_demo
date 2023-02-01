#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os
import pandas as pd
import numpy as np
import re
import pyarrow
from __future__ import division

# load autopsies
info_file_path = 'T:/Data Science Demonstration Project/Code Files/autopsies.feather'


autopsies = pd.read_feather(info_file_path)
autopsies.head()


# In[4]:


narr_re = re.compile(r'narrative.*(?=external examination)')
interp_re = re.compile(r'(conclusion|(summary of case)|(summary and (opinion|interpretation))).*')
circ_sum_re = re.compile(r'summary of circumstances.*') # postmortem observations

narrative_matches = []
for row in autopsies.itertuples():
    DID, doc = row.DID, row.doc
    
    if row.Index % 1000 == 0:
        print(row.Index)
    
    ### extract narrative that comes at beginning of autopsy and before external examination
    try:
        narr_match = narr_re.search(doc)
        narr = narr_match.group()
        narr_end = narr_match.end()
        
    except:
        narr = None
        narr_end = 0
    
    ### extract narrative that comes after internal examination and typically before toxicology report
    # start of toxicology report
    tox_match = re.search('nms labs', doc)
    if tox_match:
        tox_start = tox_match.start()
        
    if not tox_match or narr_end > tox_start:
        tox_start = len(doc) - 1
        
    try:
        interp = interp_re.search(doc[narr_end:tox_start]).group()
    except:
        interp = None
        
    ### extract summary of circumstances that sometimes is included, comes at end of report
    try: 
        circ = circ_sum_re.search(doc[narr_end:]).group()
    except:
        circ = None
        
    narrative_matches.append([DID, row.Forensic_Center, narr, interp, circ, row.File_Path])


# In[5]:


narr_df = pd.DataFrame(narrative_matches, columns = ['DID', 'Forensic_Center',
                                                     'narr', 'interp', 'circ', 'File_Path'])
#narr_df.to_feather('narratives.feather')


# In[6]:


narr_df.groupby('Forensic_Center')['DID'].nunique()


# In[7]:


for fc in ['E', 'M', 'NE', 'SE', 'W']:
    total = narr_df.loc[narr_df.Forensic_Center==fc]['DID'].nunique()
    n_narr = narr_df.loc[narr_df.Forensic_Center==fc]['narr'].notnull().sum()
    n_interp = narr_df.loc[narr_df.Forensic_Center==fc]['interp'].notnull().sum()
    n_circ = narr_df.loc[narr_df.Forensic_Center==fc]['circ'].notnull().sum()
    
    print(f'''{fc} 
    Total: {total}
    Narrative: {n_narr} ({round(n_narr/total, 3)*100})
    Interpretation: {n_interp} ({round(n_interp/total, 3)*100})
    Summary of Circumstances: {n_circ} ({round(n_circ/total, 3)*100})''')


# In[8]:


total = narr_df.loc[narr_df.Forensic_Center.isna()].shape[0]
n_narr = narr_df.loc[narr_df.Forensic_Center.isna()]['narr'].notnull().sum()
n_interp = narr_df.loc[narr_df.Forensic_Center.isna()]['interp'].notnull().sum()
n_circ = narr_df.loc[narr_df.Forensic_Center.isna()]['circ'].notnull().sum()
    
print(f'''? 
    Total: {total}
    Narrative: {n_narr} ({round(n_narr/total, 3)*100})
    Interpretation: {n_interp} ({round(n_interp/total, 3)*100})
    Summary of Circumstances: {n_circ} ({round(n_circ/total, 3)*100})
    ''')


# In[9]:


narr_df


# In[ ]:


# SE, could also look for i hereby certify that; i hereby declare that

# East, could also look up to final anatomic diagnosis
# print(did, re.findall('(.*(?=external examination))|(narrative summary of circumstances surrounding death.*$)', autopsies[did]))

## Middle/West, could also look up to pathological diagnosis/diagnoses
# Middle
# conclusion, SUMMARY OF CASE, summary of case, summary and interpretation 
# print(did, re.findall('(.*(?=external examination))|(narrative summary of circumstances surrounding death.*$)', autopsies[did]))


# In[12]:


narr_df.to_csv('C:/Users/DC20B46/Documents/narr_df.csv') 

