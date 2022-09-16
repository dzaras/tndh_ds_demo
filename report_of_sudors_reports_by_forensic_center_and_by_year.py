#!/usr/bin/env python
# coding: utf-8

# ## Convert the data in the 'sudors_autopsies_by_year_and_forensic_center.xlsx' into a table

# In[2]:


import pandas as pd
df = pd.read_excel(r'C:\Users\DC20B46\Documents\sudors_autopsies_by_year_and_forensic_center_2019-2021H1.xlsx')


# In[3]:


df.year.value_counts()


# In[13]:


len(df)


# In[4]:


crosstab1 = pd.crosstab(index = df['forensic_center'], columns = df['year'])

crosstab1


# In[5]:


pd.crosstab(df.year, df.forensic_center).plot.bar(stacked=True)

