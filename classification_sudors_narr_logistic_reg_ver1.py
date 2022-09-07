#!/usr/bin/env python
# coding: utf-8

# # Classification of SUDORS vs. Non-SUDORS Autopsy Summaries with Logistic Regression

# In[50]:


import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import seaborn as sns
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'notebook')
from sklearn.linear_model import LogisticRegression
import sklearn.model_selection
import sklearn.preprocessing as preproc
from sklearn.feature_extraction import text
import pickle
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')


# ## Import dataset with both SUDORS and Non-SUDORS autopsy narrative summaries from 2019 and 2020 

# In[2]:


narr_df = pd.read_feather(r'C:/Users/DC20B46/Documents/narr_od_nonod_2019_20.feather')


# ## Text Preprocessing

# In[3]:


def clean_text(text, remove_stopwords = True):
    '''Remove unwanted characters, stopwords, and format the text to create fewer nulls word embeddings'''
        
    # remove stop words
    if remove_stopwords:
        text = text.split()
        stops = set(stopwords.words("english"))
        text = [w for w in text if not w in stops]
        text = " ".join(text)

    # Tokenize each word
    text =  nltk.WordPunctTokenizer().tokenize(text)
        
    return text


# In[9]:


narr_df['Text_Cleaned'] = list(map(clean_text, narr_df.narr))


# In[15]:


def lemmatized_words(text):
    lemm = nltk.stem.WordNetLemmatizer()
    narr_df['lemmatized_text'] = list(map(lambda word:
                                     list(map(lemm.lemmatize, word)),
                                     narr_df.Text_Cleaned))
    

lemmatized_words(narr_df.Text_Cleaned)


# In[16]:


narr_df.head(3)


# In[19]:


bow_converter = CountVectorizer(tokenizer=lambda doc: doc, lowercase=False)
x = bow_converter.fit_transform(narr_df['Text_Cleaned'])

words = bow_converter.get_feature_names_out()
len(words)


# In[21]:


bigram_converter = CountVectorizer(tokenizer=lambda doc: doc, ngram_range=[2,2], lowercase=False) 
x2 = bigram_converter.fit_transform(narr_df['Text_Cleaned'])
bigrams = bigram_converter.get_feature_names()
len(bigrams)


# In[26]:


# bigrams[1230:1250]


# In[27]:


trigram_converter = CountVectorizer(tokenizer=lambda doc: doc, ngram_range=[3,3], lowercase=False) 
x3 = trigram_converter.fit_transform(narr_df['Text_Cleaned'])
trigrams = trigram_converter.get_feature_names()
len(trigrams)


# ## Bag of Words Transformation

# In[28]:


training_data, test_data = sklearn.model_selection.train_test_split(narr_df, train_size = 0.8, random_state=42)


# In[29]:


print(training_data.shape)
print(test_data.shape)


# In[30]:


bow_transform = CountVectorizer(tokenizer=lambda doc: doc, ngram_range=[3,3], lowercase=False) 


# In[31]:


X_tr_bow = bow_transform.fit_transform(training_data['Text_Cleaned'])


# In[32]:


len(bow_transform.vocabulary_)


# In[33]:


X_tr_bow.shape


# In[34]:


X_te_bow = bow_transform.transform(test_data['Text_Cleaned'])


# In[36]:


y_tr = training_data['od']
y_te = test_data['od']


# ## Tf-Idf Tranformation

# In[37]:


tfidf_transform = text.TfidfTransformer(norm=None)
X_tr_tfidf = tfidf_transform.fit_transform(X_tr_bow)


# In[38]:


X_te_tfidf = tfidf_transform.transform(X_te_bow)


# ## Classification with Logistic Regression

# In[39]:


def simple_logistic_classify(X_tr, y_tr, X_test, y_test, description, _C=1.0):
    model = LogisticRegression(C=_C).fit(X_tr, y_tr)
    score = model.score(X_test, y_test)
    print('Test Score with', description, 'features', score)
    return model


# In[40]:


model_bow = simple_logistic_classify(X_tr_bow, y_tr, X_te_bow, y_te, 'bow')
model_tfidf = simple_logistic_classify(X_tr_tfidf, y_tr, X_te_tfidf, y_te, 'tf-idf')


# In[41]:


param_grid_ = {'C': [1e-5, 1e-3, 1e-1, 1e0, 1e1, 1e2]}
bow_search = sklearn.model_selection.GridSearchCV(LogisticRegression(), cv=5, param_grid=param_grid_)
tfidf_search = sklearn.model_selection.GridSearchCV(LogisticRegression(), cv=5,
                                   param_grid=param_grid_)


# In[42]:


bow_search.fit(X_tr_bow, y_tr)


# In[43]:


bow_search.best_score_


# In[44]:


tfidf_search.fit(X_tr_tfidf, y_tr)


# In[45]:


tfidf_search.best_score_


# In[46]:


bow_search.best_params_


# In[47]:


tfidf_search.best_params_


# In[48]:


bow_search.cv_results_


# In[51]:


results_file = open('tfidf_gridcv_results.pkl', 'wb')
pickle.dump(bow_search, results_file, -1)
pickle.dump(tfidf_search, results_file, -1)
results_file.close()


# In[52]:


pkl_file = open('tfidf_gridcv_results.pkl', 'rb')
bow_search = pickle.load(pkl_file)
tfidf_search = pickle.load(pkl_file)
pkl_file.close()


# In[53]:


search_results = pd.DataFrame.from_dict({'bow': bow_search.cv_results_['mean_test_score'],
                               'tfidf': tfidf_search.cv_results_['mean_test_score']})
search_results


# In[54]:


get_ipython().run_line_magic('matplotlib', 'inline')
ax = sns.boxplot(data=search_results, width=0.4)
ax.set_ylabel('Accuracy', size=14)
ax.tick_params(labelsize=14)
plt.savefig('tfidf_gridcv_results.png')


# In[3]:


model_bow = simple_logistic_classify(X_tr_bow, y_tr, X_te_bow, y_te, 'bow', 
                              _C=bow_search.best_params_['C'])
model_tfidf = simple_logistic_classify(X_tr_tfidf, y_tr, X_te_tfidf, y_te, 'tf-idf', 
                              _C=tfidf_search.best_params_['C'])


# In[2]:


y_pred = simple_logistic_classify.predict(X_test)

confusion_matrix(y_te, y_pred)


# In[1]:


from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
print(classification_report(y_te, y_pred))

