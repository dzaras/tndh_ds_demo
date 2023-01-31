#!/usr/bin/env python
# coding: utf-8

# ### Script from https://medium.com/@MansiKukreja/clinical-text-negation-handling-using-negspacy-and-scispacy-233ce69ab2ac

# In[ ]:


#!pip install negspacy


# In[2]:


#!pip install spacy


# In[6]:


#!pip install scispacy


# ### Load Required Libraries

# In[1]:


import negspacy


# In[3]:


import spacy


# In[4]:


import scispacy
from spacy import displacy
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span
from negspacy.negation import Negex


# ### Load scispaCy models

# In[4]:


# !pip install en_core_sci_sm

nlp0 = spacy.load("en_core_sci_sm")


# In[5]:


nlp1 = spacy.load("en_ner_bc5cdr_md")


# ### Sample Input Clinical Note

# In[6]:


clinical_note = "Patient resting in bed. Patient given azithromycin without any difficulty. Patient has audible wheezing, states chest tightness. No evidence of hypertension.Patient denies nausea at this time. zofran declined. Patient is also having intermittent sweating associated with pneumonia. Patient refused pain but tylenol still given. Neither substance abuse nor alcohol use however cocaine once used in the last year. Alcoholism unlikely.Patient has headache and fever. Patient is not diabetic. No signs of diarrhea. Lab reports confirm lymphocytopenia. Cardaic rhythm is Sinus bradycardia. Patient also has a history of cardiac injury. No kidney injury reported. No abnormal rashes or ulcers. Patient might not have liver disease. Confirmed absence of hemoptysis. Although patient has severe pneumonia and fever , test reports are negative for COVID-19 infection. COVID-19 viral infection absent."


# ### NLP pipeline Implementation

# ### Lemmatizer — model (en_core_sci_sm)

# In[7]:


#lemmatizing the notes to capture all forms of negation(e.g., deny: denies, denying)
def lemmatize(note, nlp):
    doc = nlp(note)
    lemNote = [wd.lemma_ for wd in doc]
    return " ".join(lemNote)
lem_clinical_note= lemmatize(clinical_note, nlp0)
#creating a doc object using BC5CDR model
doc = nlp1(lem_clinical_note)


# ### Feature Extractor: Named Entities

# In[8]:


#function to modify options for displacy NER visualization
def get_entity_options():
    entities = ["DISEASE", "CHEMICAL", "NEG_ENTITY"]
    colors = {'DISEASE': 'linear-gradient(180deg, #66ffcc, #abf763)', 'CHEMICAL': 'linear-gradient(90deg, #aa9cfc, #fc9ce7)', "NEG_ENTITY":'linear-gradient(90deg, #ffff66, #ff6600)'}
    options = {"ents": entities, "colors": colors}    
    return options
options = get_entity_options()
#visualizing identified Named Entities in clinical input text 
displacy.render(doc, style='ent', options=options)


# ## Feature Extractor: Negation Detection

# In[17]:


#adding a new pipeline component to identify negation
def neg_model(nlp_model):
    nlp = spacy.load(nlp_model, disable = ['parser'])
    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    negex = Negex(nlp)
    nlp.add_pipe(negex)
    return nlp
# """
# Negspacy sets a new attribute e._.negex to True if a negative concept is encountered
# """
def negation_handling(nlp_model, note, neg_model):
    results = []
    nlp = neg_model(nlp_model) 
    note = note.split(".") #sentence tokenizing based on delimeter 
    note = [n.strip() for n in note] #removing extra spaces at the begining and end of sentence
    for t in note:
        doc = nlp(t)
        for e in doc.ents:
            rs = str(e._.negex)
            if rs == "True": 
                results.append(e.text)
    return results
# # #list of negative concepts from clinical note identified by negspacy
results0 = negation_handling("en_ner_bc5cdr_md", lem_clinical_note, neg_model)


# In[14]:


import pysbd
import spacy
from spacy.language import Language

text = "My name is Jonas E. Smith.          Please turn to p. 55."
nlp = spacy.blank('en')

@Language.component("sbd")
def pysbd_sentence_boundaries(doc):
    seg = pysbd.Segmenter(language="en", clean=False, char_span=True)
    sents_char_spans = seg.segment(doc.text)
    char_spans = [doc.char_span(sent_span.start, sent_span.end, alignment_mode="contract") for sent_span in sents_char_spans]
    start_token_ids = [span[0].idx for span in char_spans if span is not None]
    for token in doc:
        token.is_sent_start = True if token.idx in start_token_ids else False
    return doc

# add as a spacy pipeline component
nlp.add_pipe("sbd", first=True)

doc = nlp(text)
for sent in doc.sents:
    print(sent.text)


# In[16]:


# function to identify span objects of matched megative phrases from clinical note
def match(nlp,terms,label):
        patterns = [nlp.make_doc(text) for text in terms]
        matcher = PhraseMatcher(nlp.vocab)
        matcher.add(label, None, *patterns)
        return matcher
#replacing the labels for identified negative entities
def overwrite_ent_lbl(matcher, doc):
    matches = matcher(doc)
    seen_tokens = set()
    new_entities = []
    entities = doc.ents
    for match_id, start, end in matches:
        if start not in seen_tokens and end - 1 not in seen_tokens:
            new_entities.append(Span(doc, start, end, label=match_id))
            entities = [
                e for e in entities if not (e.start < end and e.end > start)
            ]
            seen_tokens.update(range(start, end))
    doc.ents = tuple(entities) + tuple(new_entities)
    return doc
matcher = match(nlp1, results0,"NEG_ENTITY")
#doc0: new doc object with added "NEG_ENTITY label"
doc0 = overwrite_ent_lbl(matcher,doc)
#visualizing identified Named Entities in clinical input text 
displacy.render(doc0, style='ent', options=options)

