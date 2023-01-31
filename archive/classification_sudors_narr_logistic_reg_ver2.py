#!/usr/bin/env python
# coding: utf-8

# # Classification of SUDORS vs. Non-SUDORS Autopsy Summaries with Logistic Regression

# In[4]:


import pandas as pd
import json
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import re
import string
import time
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from nltk.stem import PorterStemmer
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler


# In[ ]:


narr_df = pd.read_feather(r'C:/Users/DC20B46/Documents/narr_od_nonod_2019_20.feather')


# In[1]:


# Focus on narr and od only:

narr_df = narr_df[['narr', 'od']]
narr_df.head()


# ### SUDORS Autopsy Class Distribution

# In[8]:


od_count = narr_df['od'].value_counts()
od_count = od_count.sort_index()

fig = plt.figure(figsize=(10, 6))
ax = sns.barplot(od_count.index, od_count.values)
plt.title("SUDORS Narrative Summaries Distribution",fontsize = 20)
plt.ylabel('Number of Narrative Summaries', fontsize = 12)
plt.xlabel('SUDORS Narrative Summary', fontsize = 12);


# In[43]:


# baseline accuracy based on the number of SUDORS narrative summaries compared to the total number of narrative summaries
print((7288/(7288+3539)))


# ### train-test split

# In[45]:


train, test = train_test_split(narr_df, test_size = 0.2, stratify = narr_df['od'], random_state = 42)


# ## Text Preprocessing

# ### Let’s first remove all non-letter characters, punctuations, and make sure all letters are in lower-cases. Later we will also evaluate the effect of removing stopwords and stemming/lemmatization.

# In[46]:


punct = set(string.punctuation)


# In[47]:


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


# ### binary feature representation, no stopwords removal or stemming, all unigrams

# In[49]:


start_time = time.time()
cv= CountVectorizer(binary=True, analyzer = text_prep, min_df = 10, max_df = 0.95)
cv.fit_transform(train['narr'].values)
train_feature_set=cv.transform(train['narr'].values)
test_feature_set=cv.transform(test['narr'].values)
print("Time takes to convert text input into feature vector: ", round((time.time() - start_time)/60, 2), " mins")


# In[58]:


train_feature_set.shape[1] # size of the vocabulary left in our corpus


# In[51]:


cv.vocabulary_['decedent']


# In[56]:


list(cv.vocabulary_.keys())[list(cv.vocabulary_.values()).index(4512)]


# ### Fit Logistic Regression Model

# In[59]:


y_train = train['od'].values
y_test = test['od'].values


# In[60]:


start_time = time.time()
lr = LogisticRegression(solver = 'liblinear', random_state = 42, max_iter=1000)
lr.fit(train_feature_set,y_train)
y_pred = lr.predict(test_feature_set)
print("Time takes to train model and make predictions: ", round((time.time() - start_time)/60, 2), " mins")


# In[61]:


print("Accuracy: ",round(metrics.accuracy_score(y_test,y_pred),3))
print("F1: ",round(metrics.f1_score(y_test, y_pred),3))


# In[ ]:





# In[ ]:





# In[ ]:





# In[62]:


disp = metrics.plot_confusion_matrix(lr, test_feature_set, y_test,
                                 display_labels=['Class 0', 'Class 1'],
                                 cmap=plt.cm.Blues,
                                 normalize='true')
disp.ax_.set_title('Logistic Regression Confusion matrix, with normalization');


# In[65]:


feature_importance = lr.coef_[0][:10]
for i,v in enumerate(feature_importance):
    print('Feature: ', list(cv.vocabulary_.keys())[list(cv.vocabulary_.values()).index(i)], 'Score: ', v)


# In[64]:


feature_importance = lr.coef_[0]
sorted_idx = np.argsort(feature_importance)


# ### Top words for the positive class (SUDORS narrative summaries):

# In[66]:


top_10_pos_w = [list(cv.vocabulary_.keys())[list(cv.vocabulary_.values()).index(w)] for w in sorted_idx[range(-1,-11, -1)]]
print(top_10_pos_w)


# In[69]:


fig = plt.figure(figsize=(10, 6))
ax = sns.barplot(top_10_pos_w, feature_importance[sorted_idx[range(-1,-11, -1)]])
plt.title("Most Important Words Used in SUDORS narrative summaries",fontsize = 20)
x_locs,x_labels = plt.xticks()
plt.setp(x_labels, rotation = 40)
plt.ylabel('Feature Importance', fontsize = 12)
plt.xlabel('Word', fontsize = 12);


# #### Let’s check all the narrative summaries that contain the word ‘overdose’ and see how many of them are in the SUDORS class:

# In[74]:


sub_poi = train.loc[train.narr.str.contains('overdose')]
round(sub_poi.od.mean(),3)


# ### Top words for the negative class (non-SUDORS narrative summaries):

# # top_10_neg_w = [list(cv.vocabulary_.keys())[list(cv.vocabulary_.values()).index(w)] for w in sorted_idx[:10]]
# print(top_10_neg_w)

# In[76]:


fig = plt.figure(figsize=(10, 6))
ax = sns.barplot(top_10_neg_w, feature_importance[sorted_idx[:10]])
plt.title("Most Important Words Used for Positive Sentiment",fontsize = 20)
x_locs,x_labels = plt.xticks()
plt.setp(x_labels, rotation = 40)
plt.ylabel('Feature Importance', fontsize = 12)
plt.xlabel('Word', fontsize = 12);


# ## Improvement Strategies

# ### After we establish the first model, examine couple of ideas to see if our model can be further improved.

# ### 1: Decrease the probability cutoff threshold
# #### To reduce False Negatives, one intuition is to lower the cutoff threshold (default at 0.5). This would increase the recall but also decrease the precision. Therefore, we need to check if this would improve the overall F1 score:

# In[77]:


pred_proba_df = pd.DataFrame(lr.predict_proba(test_feature_set))
threshold_list = [0.3,0.4,0.45,0.5]
for i in threshold_list:
    print ('\n******** For i = {} ******'.format(i))
    Y_test_pred = pred_proba_df.applymap(lambda x: 1 if x>i else 0)
    test_f1 = round(metrics.f1_score(y_test, Y_test_pred.loc[:,1].values),3)
    print('F1: {}'.format(test_f1))


# #### F1 score seems to be relatively unaffected by changes in this threshold

# ### 2: Oversample Class 1 or undersample Class 0

# In[78]:


undersample = RandomUnderSampler(sampling_strategy='majority')
X_under, y_under = undersample.fit_resample(train_feature_set,y_train)
lr = LogisticRegression(solver = 'liblinear', random_state = 42, max_iter=1000)
lr.fit(X_under,y_under)
y_pred = lr.predict(test_feature_set)
print("Time takes to train model and make predictions: ", round((time.time() - start_time)/60, 2), " mins")
print("Accuracy: ",round(metrics.accuracy_score(y_test,y_pred),3))
print("F1: ",round(metrics.f1_score(y_test, y_pred),3))


# In[79]:


oversample = RandomOverSampler(sampling_strategy='minority')
X_over, y_over = oversample.fit_resample(train_feature_set,y_train)
lr = LogisticRegression(solver = 'liblinear', random_state = 42, max_iter=1000)
lr.fit(X_over,y_over)
y_pred = lr.predict(test_feature_set)
print("Time takes to train model and make predictions: ", round((time.time() - start_time)/60, 2), " mins")
print("Accuracy: ",round(metrics.accuracy_score(y_test,y_pred),3))
print("F1: ",round(metrics.f1_score(y_test, y_pred),3))


# ####  F1 score does not improve from oversampling or undersampling

# ### 3: Remove stopwords and stemming

# In[81]:


sw = set(stopwords.words("english"))
ps = PorterStemmer()


# In[82]:


def text_prep_stop_stem(text):
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
    
    #stem and remove stop words
    return [ps.stem(word) for word in punc_removed.split() if not word in sw]
    #return [word for word in punc_removed.split() if not word in sw]


# In[84]:


start_time = time.time()
cv= CountVectorizer(binary=True, analyzer = text_prep_stop_stem, min_df = 10, max_df = 0.95)
cv.fit_transform(train['narr'].values)
train_feature_set=cv.transform(train['narr'].values)
test_feature_set=cv.transform(test['narr'].values)
print("Time takes to convert text input into feature vector: ", round((time.time() - start_time)/60, 2), " mins")


# In[85]:


train_feature_set.shape[1]   # previously the size of the vocabulary was 5,078


# In[86]:


start_time = time.time()
lr = LogisticRegression(solver = 'liblinear', random_state = 42, max_iter=1000)
lr.fit(train_feature_set,y_train)
y_pred = lr.predict(test_feature_set)
print("Time takes to train model and make predictions: ", round((time.time() - start_time)/60, 2), " mins")
print("Accuracy: ",round(metrics.accuracy_score(y_test,y_pred),3))
print("F1: ",round(metrics.f1_score(y_test, y_pred),3))


# #### F1 score and accuracy actually decreased by a small amount

# ### 4: Use TF-IDF instead of binary representation

# In[88]:


start_time = time.time()
tfidf_v=TfidfVectorizer(use_idf=True, analyzer = text_prep, min_df = 10, max_df = 0.95)
tfidf_v.fit_transform(train['narr'].values)
train_feature_set=tfidf_v.transform(train['narr'].values)
test_feature_set=tfidf_v.transform(test['narr'].values)
print("Time takes to convert text input into feature vector: ", round((time.time() - start_time)/60, 2), " mins")


# In[89]:


start_time = time.time()
lr = LogisticRegression(solver = 'liblinear', random_state = 42, max_iter=1000)
lr.fit(train_feature_set,y_train)
y_pred = lr.predict(test_feature_set)
print("Time takes to train model and make predictions: ", round((time.time() - start_time)/60, 2), " mins")
print("Accuracy: ",round(metrics.accuracy_score(y_test,y_pred),3))
print("F1: ",round(metrics.f1_score(y_test, y_pred),3))


# ### 5: Include both unigrams and bigrams as features

# In[91]:


start_time = time.time()
cv = CountVectorizer(binary=True, min_df = 10, max_df = 0.95, ngram_range=(1,2))
cv.fit_transform(train['narr'].values)
train_feature_set=cv.transform(train['narr'].values)
test_feature_set=cv.transform(test['narr'].values)
print("Time takes to convert text input into feature vector: ", round((time.time() - start_time)/60, 2), " mins")


# In[106]:


train_feature_set.shape[1] # After we take both unigrams and bigrams (sequence of two words) into consideration, 
# we first see an increase in vocabulary size:


# In[94]:


# cv.vocabulary_


# In[2]:


start_time = time.time()
lr = LogisticRegression(solver = 'liblinear', random_state = 42, max_iter=1000)
lr.fit(train_feature_set,y_train)
y_pred = lr.predict(test_feature_set)
print("Time takes to train model and make predictions: ", round((time.time() - start_time)/60, 2), " mins")
print("Accuracy: ",round(metrics.accuracy_score(y_test,y_pred),3))
print("F1: ",round(metrics.f1_score(y_test, y_pred),3))
print("precision",round(metrics.precision.precision_score(y_test, y_pred)))


# In[102]:


disp = metrics.plot_confusion_matrix(lr, test_feature_set, y_test,
                                 display_labels=['Class 0', 'Class 1'],
                                 cmap=plt.cm.Blues,
                                 normalize='true')
disp.ax_.set_title('Logistic Regression Confusion matrix, with normalization');


# #### After fitting this model, we see improvements in both metrics, especially in F1 score.

# In[96]:


feature_importance = lr.coef_[0][:10]
for i,v in enumerate(feature_importance):
    print('Feature: ', list(cv.vocabulary_.keys())[list(cv.vocabulary_.values()).index(i)], 'Score: ', v)


# #### The new top 10 features for both SUDORS and non-SUDORS narrative summaries again

# In[97]:


feature_importance = lr.coef_[0]
sorted_idx = np.argsort(feature_importance)
top_10_pos_w = [list(cv.vocabulary_.keys())[list(cv.vocabulary_.values()).index(w)] for w in sorted_idx[range(-1,-11, -1)]]
print(top_10_pos_w)


# In[98]:


top_10_neg_w = [list(cv.vocabulary_.keys())[list(cv.vocabulary_.values()).index(w)] for w in sorted_idx[:10]]
print(top_10_neg_w)


# In[100]:


fig = plt.figure(figsize=(10, 6))
ax = sns.barplot(top_10_pos_w, feature_importance[sorted_idx[range(-1,-11, -1)]])
plt.title("Most Important Words Used in SUDORS Narrative Summaries",fontsize = 20)
x_locs,x_labels = plt.xticks()
plt.setp(x_labels, rotation = 40)
plt.ylabel('Feature Importance', fontsize = 12)
plt.xlabel('Word', fontsize = 12);


# In[101]:


fig = plt.figure(figsize=(10, 6))
ax = sns.barplot(top_10_neg_w, feature_importance[sorted_idx[:10]])
plt.title("Most Important Words Used in Non-SUDORS Narrative Summaries",fontsize = 20)
x_locs,x_labels = plt.xticks()
plt.setp(x_labels, rotation = 40)
plt.ylabel('Feature Importance', fontsize = 12)
plt.xlabel('Word', fontsize = 12);


# In[ ]:




