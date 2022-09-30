#!/usr/bin/env python
# coding: utf-8

# # An attempt at Negation Detection from the https://github.com/xiaoqingwan/negation_detection_nlp/blob/main/negation.ipynb

# ### Installation

# In[7]:


# import sys
# !{sys.executable} -m pip install spacy
# !{sys.executable} -m pip install negspacy
# !pip install spacy-stanza 
# !pip install pandas
# # This package wraps the Stanza (formerly StanfordNLP) library, so you can use Stanford's models in a spaCy


# In[1]:


import spacy # to build a nlp pipeline
import stanza # for named entity recognition
# this package wraps Stanza around Spacy, so that we can use Stanza in a spaCy pipeline.
import spacy_stanza
from negspacy.negation import Negex
from negspacy.termsets import termset # to customize negation terms
import pandas as pd


# In[2]:


print(stanza.__version__)
print(spacy.__version__)


# ### Set up NLP pipeline

# In[19]:


# download and initialize a mimic pipeline with an i2b2 NER model
# stanza.download('en', package='mimic', processors={'ner': 'i2b2'})
nlp = spacy_stanza.load_pipeline('en', package='mimic', processors={'ner': 'BC5CDR'})


# ### Add customized terms to the default list of terms

# In[4]:


ts = termset("en_clinical")
# customize the term list by adding more negation terms
ts.add_patterns({
            'preceding_negations': ['abstain from','other than','except for','except','with the exception of',
                                    'excluding','lack of','contraindication','contraindicated','interfere with',
                                   'prohibit','prohibits', 'no history of'],
            'following_negations':['negative','is allowed','impossible','exclusionary']
        })


# ### Let negex know what entities we are extracting

# In[20]:


nlp.add_pipe("negex", config={"ent_types":['DISEASE','CHEMICAL']})


# ### Importing the SUDORS reports 

# In[7]:


df = pd.read_feather(r'C:\Users\DC20B46\Documents\narratives_sudors_2019-2022_09.02.22.feather') # data from '19-'22


# In[ ]:


df19 = df[df.year == '2019']


# In[9]:


df19.full_narr.head()


# In[37]:


first_full_narr = df19["full_narr"].iloc[1]
print(first_full_narr)


# In[33]:


#df19['result1'] = df19['full_narr'].apply(lambda x: nlp()) 

doc = nlp('narrative summary 01/03/2019 11 :47 am 6622 rollingbrook lane, apartment 1, memphis, tn 38134 i type of death suspected overdose 3456 lamar ave. rm 138, memphis 38118, tn state number: 19-79-0021 case number: mec2019-0015 sex i date of birth i 11/20/1987 female age i 31 years race black agency/complaint#: i investigating memphis police department, complaint#: 1901001119me reportedly this 31 year-old female black, identified as shanika jones, was discovered unresponsive in her secured hotel room by hotel staff who contacted 911 emergencies. memphis police department and memphis fire department unit 34 responded to the scene located at 3456 lamar avenue at the deluxe inn and suites. paramedic k. curry confirmed asystole at 1147 hours. this office was notified of the death at 1220 hours by officer m. collins who stated the death was a suspected overdose. jurisdiction for the death was accepted by the medical examiner office. i responded to the scene where a brief body examination was performed and the decedent and scene were documented with photography. the decedent was transported to the west tennessee regional forensic center for further examination, positive identification, and final disposition to the funeral home. lindsey n price, investigator 1/3/2019 summary and interpretation was a 31 year old female with a medical history of bipolar stress motel room. she was admitted the decedent posttraumatic in her secured having a mental break down. on admission paraphernalia who was reportedly to alliance was discovered and depression disorder, at the scene. crisis found unresponsive center on 1/1/2019 for she denied any suicidal ideation. drug disorder, autopsy revealed pulmonary edema and abrasions on the face and knees. toxicological studies alprazolam, performed and methamphetamine. on postmortem fentanyl, iliac blood detected benzoylecgonine, death was caused by alprazolam, of the death scene investigation, death, and autopsy methamphetamine, and fentanyl intoxication. reports circumstances surrounding and leading up to the findings indicate the manner of death to be accident')
for e in doc.ents:
    print(e.text, e._.negex)
    


# In[34]:


doc.ents


# In[39]:


doc = nlp(df19.full_narr.iloc[2])
for e in doc.ents:
    print(e.text, e._.negex)


# In[43]:


df19.shape


# In[31]:


doc = nlp('Patient had a headache, but no fever')

doc.ents
# for e in doc.ents:
# 	print(e.text, e._.negex)


# In[41]:


from spacy import displacy

#function to modify options for displacy NER visualization
def get_entity_options():
    entities = ["DISEASE", "CHEMICAL", "NEG_ENTITY"]
    colors = {'DISEASE': 'linear-gradient(180deg, #66ffcc, #abf763)', 'CHEMICAL': 'linear-gradient(90deg, #aa9cfc, #fc9ce7)', "NEG_ENTITY":'linear-gradient(90deg, #ffff66, #ff6600)'}
    options = {"ents": entities, "colors": colors}    
    return options
options = get_entity_options()
#visualizing identified Named Entities in clinical input text 
displacy.render(doc, style='ent', options=options)

