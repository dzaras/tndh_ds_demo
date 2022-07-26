#!/usr/bin/env python
# coding: utf-8

# # Random Forest Classification for SUDORS Variables

# In[1]:


import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


# #### Import autopsy dataset from 2019-20 

# In[2]:


narr1920_df = pd.read_feather(r'C:/Users/DC20B46/Documents/narr_od_nonod_2019_20.feather')
narr1920_df.shape


# In[3]:


# Focus on narr and od only:
narr1920_df = narr1920_df[['narr', 'od']]
narr1920_df.head(2)


# #### Write a function to clean sentences

# In[4]:


import string
import nltk
#ps = nltk.PorterStemmer()
stopwords= nltk.corpus.stopwords.words('english')

def clean(sentence):
    s = "".join(x for x in sentence if x not in string.punctuation)
    temp = s.lower().split(' ')
    temp2 = [x for x in temp if x not in stopwords]
    return temp2
clean("hell peOople  are hOOow ! AAare ! you. enough.. are")


# #### Create Vectorizer and Transform into Column Features

# In[11]:


from sklearn.feature_extraction.text import TfidfVectorizer

vect = TfidfVectorizer(analyzer=clean)
vector_output = vect.fit_transform(narr1920_df['narr'])

print(vect.get_feature_names()[0:100])


# In[10]:


# print (vector_output [0:10])


# In[8]:


pd.DataFrame(vector_output.toarray())


# In[12]:


x_features = pd.DataFrame(vector_output.toarray())


# In[14]:


from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support as score

x_train, x_test, y_train, y_test = train_test_split(x_features,narr1920_df['od'])
rf = RandomForestClassifier(n_estimators=100,max_depth=None,n_jobs=-1)
rf_model = rf.fit(x_train,y_train)
sorted(zip(rf_model.feature_importances_,x_train.columns),reverse=True)[0:20]


# In[17]:


y_pred=rf_model.predict(x_test)
precision,recall,fscore,support =score(y_test,y_pred,pos_label=1, average ='binary')
print('Precision : {} / Recall : {} / fscore : {} / Accuracy: {}'.format(round(precision,3),round(recall,3),round(fscore,3),round((y_pred==y_test).sum()/len(y_test),3)))

