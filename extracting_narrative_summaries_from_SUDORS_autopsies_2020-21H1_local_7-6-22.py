#!/usr/bin/env python
# coding: utf-8

# # Extracting narrative summaries from confirmed SUDORS autopsies (from 2020H1,H2, 2021H1) downloaded to local folder - 7-6-22

# In[2]:


import os
import pandas as pd
import numpy as np
import re


# #### FIrst, concatenate the 2020H1 and 2020H2 sudors autopsies datasets we created from the equivalent directories

# In[7]:


df = pd.read_excel(r'C:\Users\DC20B46\Documents\autopsies_sudors_clean_2020-21_local.xlsx')


# In[8]:


df.shape


# #### Now, begin the narrative summary extraction

# In[3]:


# The following line is not necessary here because we only have autopsies from one year (2021) instead of two or more
# df1['Year'] = df1['DID'].str[:4] # extract the first four digits of DID to identify year 


# In[9]:


df.head(3)


# In[11]:


### remove newlines and extra spaces
def rm_whitespace(doc):
    
    rm_newlines = ' '.join(doc.split('\n'))
    rm_newlines_spaces = ' '.join(rm_newlines.split())
    
    return rm_newlines_spaces

### clean text: lowercase, remove whitespace, symbols
symbols = '�¥•°·□§Â®â€™µα_'
def rm_whitespace_sym(doc_text):
    
    doc_text = doc_text.lower()
    text_clean = rm_whitespace(doc_text)
    #text_clean = re.sub(pattern = all_re, repl = '', string = text_clean)
    text_clean = "".join([char for char in text_clean if char not in symbols])
    #text_clean = rm_whitespace(text_clean)
    
    return text_clean

### assign forensic center
def get_forensic_center(doc_text):
    
    if re.search('center for forensic medicine', doc_text):
        return 'M'
    
    elif re.search('(office of the medical examiner west)|(west tennessee( regional forensic center)?)', doc_text):
        return 'W'
    
    elif re.search('(william l jenkins)|(quillen college)|(east tennessee state)', doc_text):
        return 'NE'
    
    elif re.search('(knox county)|(sevier county)|(regional (forensic( center)? )?knox)', doc_text):
        return 'E'
   
    elif re.search('hamilton county( forensic center)?', doc_text):
        return 'SE'
    else:
        return None

#     # load mastercaselist of SUDORS cases
#     sudors = pd.read_excel('E:\Data Science Demonstration Project\mastercaselist.xlsx')
#     sudors['DID'] = sudors['DID'].astype(str)
#     sudors = sudors.loc[sudors.autopsy==1]

#     # load duplicate reports
#     duplicate_reports = pd.read_csv('E:\Data Science Demonstration Project\Code Files\duplicate_autopsies.csv')
#     duplicate_reports['DID'] = duplicate_reports['DID'].astype(str)
#     rm_reports = duplicate_reports.loc[duplicate_reports.Keep==0]

#     # load all autopsies
#     autopsies_all = pd.read_feather('autopsies_original.feather')
#     autopsies = autopsies_all.loc[autopsies_all.File_Path.str.contains('A:/20(?:19|20)', regex = True)].reset_index(drop=True)

#     # remove duplicate autopsies
#     autopsies_uniq = autopsies.merge(rm_reports[['DID', 'File_Path']], how='outer', indicator = True)
#     autopsies_uniq = autopsies_uniq.loc[autopsies_uniq._merge == 'left_only'].reset_index(drop=True).drop(columns='_merge')

#     # keep sudors autopsies
#     sudors_autopsies = autopsies_uniq.merge(sudors, how = 'inner').drop(columns = ['Incident_Number', 'autopsy', 'File_Path'])
#     print(sudors_autopsies.shape, sudors_autopsies.DID.nunique())

#    sudors_autopsies.head()


# In[12]:


df['doc_clean'] = df['doc'].apply(rm_whitespace_sym)

df['forensic_center'] = df['doc_clean'].apply(get_forensic_center)
df['forensic_center'].fillna('', inplace = True)

df.shape


# In[13]:


df.head(3)


# # Extract Narrative Sections Based on Forensic Center

# Narrative Text from Three Sections:
# 
# (1) Narrative = starting from "narrative" or "summary" or for NE "brief history"; ends at different points depending on forensic center:
# 
# - M/W: jurisdiction accept, toxicology order, autopsy order, yes, approve, external exam<br>
# - E: final anatomic diag, external exam<br>
# - NE: signature, external exam, autopsy exam<br>
# - SE: no narrative section<br>
# 
# (2) Interpretation (M/W only) = Section beginning with conclusion, summary, summary and opinion, summary and interpretation, summary and comment (search space = from where narrative ends, to beginning of toxicology or 'nms labs')
# 
# 
# (3) Circumstances = "summary of ci[rcumstances]" to end of autopsy
# 

# In[14]:


### all formats except SE should have initial narrative section
# regex for start of narrative
narr_start_re = re.compile(r'(?<!analysis )(narrative|summary).*')
narr_start_re_NE = re.compile(r'(?<!analysis )(narrative|summary|brief\s?history).*')

# regex for end of narrative
narr_re_end = dict()
narr_re_end['M'] = narr_re_end['W'] = re.compile(r'''(jurisdiction\s?accept|toxicology\s?order|
autopsy\s?order|yes|approve|external\s?exam)''', re.X)
narr_re_end['E'] = re.compile(r'(final\s?anatomic\s?diag|external\sexam)')
narr_re_end['NE'] = re.compile(r'(signature|(external|autopsy)\s?exam)')

def get_narr(doc, fc):
    # no narratives in SE
    if fc not in narr_re_end.keys():
        return np.nan, 0
    
    # locate start of narrative summary
    try:
        if fc == 'NE':
            narr_match_start = narr_start_re_NE.search(doc)
        else:
            narr_match_start = narr_start_re.search(doc)
            
        narr_start = narr_match_start.start()
        
    except:
        return np.nan, 0
    
    # locate end of narrative summary
    narr_match_end = [f.start() for f in narr_re_end[fc].finditer(doc) if f.start() >= narr_start]
    if narr_match_end:
        narr_end = min(narr_match_end)
    else:
        narr_end = len(doc) - 1
    
    narr = doc[narr_start:narr_end]
    
    return narr, narr_end

### all formats may have summary of circumstances
circ_sum_re = re.compile(r'(s\s?u\s?m\s?m\s?a\s?r\s?y\s?of\s?ci).*')
def get_circ(doc, narr_end):
    try:
        circ_match = circ_sum_re.search(doc[narr_end:])
        circ = circ_match.group()
        circ_start = circ_match.start()
        return circ, circ_start
    
    except:
        return np.nan, len(doc) - 1

### W, M have interpretation section
interp_re = re.compile(r'(s\s?u\s?m\s?m\s?a\s?r\s?y(\s?and\s?(opinion|interpretation|comment))?|conclusion\b).*')
def get_interp(doc, narr_end, circ_start, fc):
    
    if fc not in ['M', 'W']:
        return np.nan
    
    # start of toxicology report
    tox_match = re.search('nms labs', doc)
    if tox_match:
        tox_start = tox_match.start()

    if not tox_match or narr_end > tox_start:
        tox_start = circ_start

    interp = interp_re.search(doc[narr_end:tox_start])
    
    try:
        return interp.group()
    except:
        return np.nan 


# In[16]:


narrative_matches = []
for row in df.itertuples():
    DID, doc, fc = row.DID, row.doc_clean, row.forensic_center

    ### extract narrative that comes at beginning of autopsy and before external examination
    narr, narr_end = get_narr(doc, fc)

    ### extract summary of circumstances that sometimes is included, comes at end of report
    circ, circ_start = get_circ(doc, narr_end)
        
    ### extract narrative that comes after internal examination and before toxicology report
    interp = get_interp(doc, narr_end, circ_start, fc)
        
    narrative_matches.append([DID, fc, row.Year, row.doc_clean, narr, interp, circ])

narr_df = pd.DataFrame(narrative_matches, columns = ['DID', 'forensic_center', 'year', 'doc_clean',
                                                     'narr', 'interp', 'circ'])

narr_df['has_narr'] = narr_df['narr'].apply(lambda x: 1 if pd.notna(x) and x != '' else 0)
narr_df['has_interp'] = narr_df['interp'].notna().astype(int)
narr_df['has_circ'] = narr_df['circ'].notna().astype(int)

narr_df['narr'].fillna('', inplace = True)
narr_df['circ'].fillna('', inplace = True)
narr_df['interp'].fillna('', inplace = True)

narr_df['full_narr'] = narr_df['narr'].astype(str) + narr_df['interp'].astype(str) + narr_df['circ'].astype(str)
narr_df['full_narr_len'] = narr_df['full_narr'].apply(len)

# remove text after postmortem observations
narr_df['circ'] = narr_df['circ'].apply(lambda x: re.sub(string=x, pattern='postmortem obs.*', repl=''))

narr_df.groupby('forensic_center').agg({'DID': 'nunique',
                                        'has_narr': 'sum',
                                        'has_interp': 'sum',
                                        'has_circ': 'sum',
                                        'full_narr_len': ['min', 'max', 'mean']})


# In[17]:


list(narr_df.columns)


# In[18]:


narr_df.to_feather('narratives_sudors_2020-21H1_local.feather')


# In[19]:


narr_df.to_excel('narratives_sudors_2020-21H1_local.xlsx')

