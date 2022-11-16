#!/usr/bin/env python
# coding: utf-8

# # Support Vector Machine Classification for SUDORS Autopsies

# In[37]:


import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import roc_auc_score
from sklearn.metrics import precision_recall_fscore_support

import string
import json
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import re
import time


# #### Import different datasets for the train and test sets  instead of splitting the same dataset into a train and test set 

# In[38]:


narr1920_df = pd.read_feather(r'C:/Users/DC20B46/Documents/narr_od_nonod_2019_20.feather')
narr1920_df.columns


# In[39]:


narr21_df = pd.read_feather(r'C:/Users/DC20B46/Documents/narr_sudors_nonsudors_2021H1.feather')
narr21_df.shape


# In[40]:


dfs = [narr1920_df, narr21_df]
c = pd.concat(dfs)


# In[41]:


c.head(3)


# In[52]:


c.groupby('forensic_center').agg({'DID': 'nunique', 'year':'sum'})


# In[55]:


grouped_df = c.groupby(['forensic_center', 'year', 'od']
                          ).size().reset_index(name="Count")


# In[56]:


print(grouped_df)


# In[4]:


# Focus on narr and od only:
narr1920_df = narr1920_df[['narr', 'od']]
narr1920_df.head(2)


# In[5]:


narr21_df = narr21_df[['narr', 'od']]
narr21_df.head(2)


## Text Preprocessing

# In[6]:


punct = set(string.punctuation)


# In[7]:


def text_prep(text):
    #clean text
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    
    #remove non-letters and lower case
    text = re.sub('[^a-z\s]', '', text.lower())
    
    #remove punctuation        
    punc_removed = [char for char in text if char not in punct]
    punc_removed = ''.join(punc_removed)
    
    return [word for word in punc_removed.split()]


# In[8]:


X = narr1920_df.iloc[:,0]
X


# In[9]:


y = narr1920_df.iloc[:,-1]
y


# In[10]:


vectorizer = CountVectorizer(stop_words='english')
X_vec = vectorizer.fit_transform(X)


# In[11]:


X_vec = X_vec.todense()
X_vec


# In[12]:


tfidf = TfidfTransformer() # by default applies "l2" normalization
X_tfidf = tfidf.fit_transform(X_vec)
X_tfidf = X_tfidf.todense()
X_tfidf


# In[13]:


X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, 
                                                    test_size = 0.20, 
                                                    random_state = 0)


# In[14]:


classifier = SVC(kernel='linear')
classifier.fit(X_train, y_train)


# In[19]:


y_pred = classifier.predict(X_test)

confusion_matrix(y_test, y_pred)


# In[20]:


confusion_matrix(y_test, y_pred, normalize = "true")


# In[26]:


f1_score(y_test, y_pred)


# In[58]:


precision_score(y_test, y_pred)


# In[59]:


recall_score(y_test,y_pred)


# In[60]:


f1_score(y_test,y_pred)


# In[57]:


from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
print(classification_report(y_test, y_pred))


# In[61]:


accuracy_score(y_test,y_pred)

