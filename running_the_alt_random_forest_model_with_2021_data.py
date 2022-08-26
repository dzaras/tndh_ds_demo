#!/usr/bin/env python
# coding: utf-8

# In[19]:


import numpy as np
import re
import nltk
import string
from sklearn.datasets import load_files
nltk.download('stopwords')
import pickle
from nltk.corpus import stopwords
import pandas as pd


# In[2]:


# Loading the trained model
with open('text_classifier', 'rb') as training_model:
    model = pickle.load(training_model)


# In[3]:


# Import the 2021 SUDORS and Non-SUDORS dataset to get predictions for that dataset
narr21_df = pd.read_feather(r'C:/Users/DC20B46/Documents/narr_sudors_nonsudors_2021H1.feather')


# In[6]:


narr21_df.shape


# In[7]:


y2 = narr21_df.od

X2 = narr21_df.drop(labels='od', axis=1)


# In[10]:


X2.shape


# ### Text Pre-Processing

# In[20]:


punct = set(string.punctuation)


# In[21]:


def clean_text(text, remove_stopwords = True):
    '''Remove unwanted characters, stopwords, and format the text to create fewer nulls word embeddings'''
        
    # remove stop words
    if remove_stopwords:
        text = text.split()
        stops = set(stopwords.words("english"))
        text = [w for w in text if not w in stops]
        text = " ".join(text)
    #remove non-letters and lower case
    text = re.sub('[^a-z\s]', '', text.lower())
    
    #remove punctuation        
    punc_removed = [char for char in text if char not in punct]
    punc_removed = ''.join(punc_removed)
    
    # Tokenize each word
    text =  nltk.WordPunctTokenizer().tokenize(text)
        
    return text


# In[22]:


X2['Text_Cleaned'] = list(map(clean_text, X2.narr))


# In[23]:


X2['Text_Cleaned'][1]


# In[24]:


def lemmatized_words(text):
    lemm = nltk.stem.WordNetLemmatizer()
    X2['lemmatized_text'] = list(map(lambda word:
                                     list(map(lemm.lemmatize, word)),
                                     X2.Text_Cleaned))
    
lemmatized_words(X2.Text_Cleaned)


# In[29]:


X2.lemmatized_text.head(2)


# ### Converting Text to Numbers

# In[31]:


X2.lemmatized_text = X2.lemmatized_text.astype(str)


# In[32]:


# using TF-IDF without having first converted to bag-of-words

from sklearn.feature_extraction.text import TfidfVectorizer
tfidfconverter = TfidfVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
X2 = tfidfconverter.fit_transform(X2['lemmatized_text']).toarray()


# In[34]:


# In this case I am using the entire dataset as a test set, since the model has been trained with the 2019-20 data
X2_test = X2


# In[35]:


y2_test = y2


# In[36]:


y2_pred = model.predict(X2_test)


# In[37]:


y2_pred.size


# In[40]:


from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

print(confusion_matrix(y2_test, y2_pred))
print(classification_report(y2_test, y2_pred))
print(accuracy_score(y2_test, y2_pred)) 


# In[41]:


unique, frequency = np.unique(y2_pred,
                              return_counts = True) 
  
# convert both into one numpy array
count = np.asarray((unique, frequency ))
  
print("The values and their frequency are:\n",
     count)

