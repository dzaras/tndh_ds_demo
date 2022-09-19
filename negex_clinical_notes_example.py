#!/usr/bin/env python
# coding: utf-8

# ### Setting Up

# In[ ]:


# this notebook is based on this article: https://towardsdatascience.com/clinical-notes-the-negative-story-e1140dd275c7


# In[1]:


#!pip install scispacy
#pip install negspacy
#pip install  en_ner_bc5cdr_md


# In[4]:


import spacy
# import scispacy
from spacy import displacy
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span
from negspacy.negation import Negex

nlp = spacy.load("en_core_sci_sm")


# In[16]:


import spacy
from negspacy.negation import Negex


# ### Specify the model and the clinical notes

# In[17]:


#Corpus on which the model is trained
nlp = spacy.load("en_ner_bc5cdr_md")

# bc5_model = "en_ner_bc5cdr_md"

#Sample clinical note
clinical_note="Patient is a 60 year old having difficuly in breathing. Not diabetic. He feels that he has been in good health until this current episode. Appetite - good. No chest pain. No weight loss or episodes of stomach pain. Hypertension absent."


# ### Extraction of Negation Entities

# In[5]:


#Adding a new pipeline component to identify negation

def negation_model(nlp_model):
    nlp = spacy.load(nlp_model)
    negex = Negex(nlp)
    nlp.add_pipe(negex)
    return nlp

#Identifying negation entities

def get_negation_entities(nlp_model, text, negation_model):
    results = []
    #Set up negex in the pipeline
    nlp = negation_model(nlp_model)
    #Split up the note into sentences (use . as the delimiter)
    text = text.split(".")
    
    #Aggregate all the negative entities in a list
    for sentence in text:
        doc = nlp(sentence)
        for e in doc.ents:
            test = str(e._.negex)
            if test == "True":
                results.append(e.text)
    return results


# In[8]:


#Get the list of negative entities from clinical note identified
final_results = get_negation_entities(bc5_model, clinical_note, negation_model)

#Print the list of negative identities
print(final_results)

