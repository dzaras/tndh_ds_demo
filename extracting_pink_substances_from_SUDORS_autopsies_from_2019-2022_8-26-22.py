#!/usr/bin/env python
# coding: utf-8

# # Extracting 'pink substances' from SUDORS Autopsies (local copies) from full_narr from 2019-2022 - 26/8/22

# In[151]:


import pandas as pd
import numpy as np
import os
import re
import copy
os.chdir("C:/Users/DC20B46/Documents")


# In[152]:


# read in the narr_df file where we have the scraped narratives from the autopsy reports downloaded locally
narr_df = pd.read_feather(r'C:\Users\DC20B46\Documents\narratives_sudors_2020-21H1_local.feather') # data from '19-'20


# In[153]:


narr_df.columns


# In[154]:


narr_df['narr'] = narr_df['narr'].astype('string')


# In[155]:


narr_df['year'] = narr_df['year'].astype(int)


# In[156]:


narr_df.dtypes


# In[157]:


narr_df.year.value_counts()


# In[158]:


len(narr_df.narr)


# ### For loop measuring how many times the term 'pink' appears in the narr_df.narr column of a dataframe

# In[163]:


string_to_match = "pink "
count = 0

for i, row in narr_df.iterrows():
    if string_to_match in narr_df.narr[i]:
        count = count + 1
        #count = 1
    else:
        #count = 0
        count = count
        
print(count)


# ### For loop that identifies the indices of the documents that contain the term 'pink' in the narrative summary (narr_df.narr) colum

# In[164]:


string_to_match = "pink "
pink_match = []

for i,row in narr_df.iterrows():
    if string_to_match in narr_df.narr[i]:
        pink_match.append(i)
print("Indices of documents that contain the term 'pink' in the narrative summary:", pink_match)


# In[165]:


narr_df.narr[318]


# ## Create a new column with dummy variable for measuring occurrence of the term 'pink' 

# In[166]:


# first, add the column and assign the value 0 to all of the rows.
narr_df['pink'] = 0


# In[167]:


narr_df.columns.get_loc("pink")   # the index of the 'pink' column in the dataframe


# ### Create a for loop to assign the value '1' to the document rows of the dataframe that contain the word 'pink' according to the pink_match list we got above

# In[169]:


for i in pink_match:
    narr_df.iloc[i, 12] = 1


# In[171]:


narr_df.iloc[118, 12]


# In[172]:


narr_df.pink.value_counts()  # there are 15 occurrences of the value '1', which is what we'd expect from our results earlier


# In[173]:


narr_df.columns


# ## Subset original dataframe to extract only rows where the term 'pink' appears

# In[175]:


df2 = narr_df[narr_df["pink"] == 1]


# In[176]:


df2.shape


# ### Save the narr_df dataframe with the added 'pink' column as a new feather and csv file

# In[178]:


narr_df.to_feather('extracted_variables_from_SUDORS_narratives_2020-2021h1_added_pink_column.feather')
# I got an error 'permission denied' when trying to save the feather file in the Code Files folder


# In[179]:


# saving the dataframe with bigram term counts as a spreadsheet
narr_df.to_excel("extracted_variables_from_local_SUDORS_narratives_2020-21h1_added_pink_column.xlsx")


# ### Save the smaller dataframe that contains only the cases where the term 'pink' appears

# In[180]:


df2.to_feather('pink_substances_SUDORS_narratives_2020-2021h1.feather')


# In[181]:


df2.to_excel('pink_substances_SUDORS_narratives_2020-2021h1.xlsx')

