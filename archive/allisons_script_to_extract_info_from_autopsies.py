#!/usr/bin/env python
# coding: utf-8

# In[2]:


# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 08:09:35 2020

@author: DC20920
"""



#%%
# =============================================================================
# This cell performs setup:
    # Installs packages
    # Reads in needed files
# =============================================================================

# Open needed libraries
import os
import pdfquery
from timeit import default_timer as timer
#from lxml import etree
from io import StringIO

from pdfminer.converter import TextConverter
#from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import pandas as pd
import numpy as np

#os.chdir("C:/Users/DC20920/Documents/Automate_Toxicology/PDFs")

#pdfOrigs = os.listdir("C:/Users/DC20920/Documents/Automate_Toxicology/PDFs")

os.chdir("W:/03.07.22")

pdfOrigs = os.listdir()

pdfOrigs = [pdf for pdf in pdfOrigs if "Autopsy" in pdf]


# In[ ]:


#%% Defining Functions
# =============================================================================
# This cell defines needed functions for analysis
# =============================================================================

# Function to identify the page of "Detailed Findings"
def find_page(filename, detailed):
    pdfFile = open(filename, 'rb')

    output_st = StringIO()
    
    parser = PDFParser(pdfFile)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, output_st, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)
        
    def extract_text_by_page(pdf_file):
        for page in PDFPage.get_pages(pdf_file,
                                      caching=True,
                                      check_extractable=True):
            rsrcmgr=PDFResourceManager()
            file_handle=StringIO()
            converter = TextConverter(rsrcmgr, file_handle)
            page_interpreter=PDFPageInterpreter(rsrcmgr, converter)
            page_interpreter.process_page(page)
            text = file_handle.getvalue()
            yield text
    
    df = pd.DataFrame(columns= ['Page', 'Text', 'NMS', 'StartTox'])
    i = 0 
           
    for page in extract_text_by_page(pdfFile):
        df.loc[i,'Text'] = page
        df.loc[i, 'Page'] = i
        df.loc[i, 'NMS'] = page.find('NMS') != -1
        
        if detailed:
            df.loc[i, 'StartTox'] = page.find("Detailed Findings: ") != -1
            df.loc[i, 'End'] = page.find("Other than the above findings, ") != -1
            
        else:
            df.loc[i, 'StartTox'] = page.find("Positive Findings") != -1
            df.loc[i, 'End'] = page.find("See Detailed Findings section for additional ") != -1
        
        i = i+1
    
    if len(df[df.StartTox==True]['Page']!=0):
        pagenum = df[df.StartTox==True]['Page'].values[0]
    elif len(df[df.End==True]['Page'])!=0:
        pagenum = df[df.End==True]['Page'].values[0]
    elif len(df[df.Text!=''])==0:
        print("No text in " + pdfFile)
        return -3
    elif len(df[df.NMS==True]) == 0:
        print("Not NMS: " + filename)
        return -2
    else:
        print("No values!")
        return -1
    
    pdfFile.close()
    return pagenum


# In[ ]:


# Function to pull detailed findings table:
def findings_tab(filename,page):
    pdf = pdfquery.PDFQuery(filename)
    pdf.load(pagenum)
    unconf = False
    #selector = pdf.pq('LTTextLineHorizontal:contains("Findings:")')
    select2 = pdf.pq('LTTextLineHorizontal:contains("See Detailed")')
    if select2.attr('y1') == None:
        select2 = pdf.pq('LTTextLineHorizontal:contains("Detailed")')
    
    y0 = float(select2.attr('y1')) +5
    #x0 = float(selector.attr('x0'))
    
    # Pull analysis test names
   # analysis = pdf.pq('LTTextLineHorizontal:contains("Compound")')
    #if analysis.attr('y0') == None :
    analysis = pdf.pq('LTTextLineHorizontal:contains("Findings:")')
    y1 = float(analysis.attr('y0')) - 30
    x0 = float(analysis.attr('x0'))
    width1 = 200
        
    # else:
    #     y1 = float(analysis.attr('y0'))
    #     x0 = float(analysis.attr('x0'))-10
    #     width1 = float(analysis.attr('width'))
    
    
    test_orig = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s,%s,%s,%s")' % (x0,y0,x0+width1,y1))
    
    Test = []
    Coords = []
    for d in test_orig.items():
        if "Urea Nitrogen" in d.text():
            Test.append(d.text())
            Coords.append(float(d.attr('y0')))
        elif "unconfirmed screen" in d.text() or "Positive" in d.text():
            unconf = True
            continue
        elif d.text().startswith("-") or d.text().startswith("Free") or d.text().startswith("("):
            continue
        elif "Hydroxyrisperidone" in d.text() and "9-" not in d.text():
            continue
        elif "Total" == d.text() or "I" == d.text():
            continue
        elif len(d.text()) < 4:
            continue
        elif "Compound" in d.text():
            continue
        elif "Results" in d.text():
            continue
        elif d.text()=="(BAC)" or d.text()=="BAG":
            continue
        elif d.text()!= "Blood Alcohol" and "Concentration" not in d.text() and d.text() != "Free" and "Analysis" not in d.text() and not d.text().startswith("Fluid"):
            Test.append(d.text())
            Coords.append(float(d.attr('y0')))
        elif "Blood Alcohol" in d.text():
            Test.append("Blood Alcohol Concentration (BAC)")
            Coords.append(float(d.attr('y0')))
        
    Test_df = pd.DataFrame([Test, Coords]).transpose().sort_values(by = 1, ascending=False)
        
   


# In[ ]:


# Pull in results
 results = pdf.pq('LTTextLineHorizontal:contains("Result")')
 
 if results.attr('y0') == None :
     #y1 = float(analysis.attr('y0')) - 50
     x0 = x0 + width1
     width1 = 90
 else:
     x0 = float(results.attr('x0'))-2
     width1 = float(results.attr('width'))
 
 result_orig = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s,%s,%s,%s")' % (x0,y0,x0+width1,y1))
 
 Results = []
 Coords = []
 for d in result_orig.items():
     if d.text() in Test:
         continue
     if "unconfirmed screen" in d.text():
         unconf = True
         continue
     
     if "Result" not in d.text() and "Analysis" not in d.text():
         Results.append(d.text())
         Coords.append(float(d.attr('y0')))

 Results_df = pd.DataFrame([Results, Coords]).transpose().sort_values(by = 1, ascending=False)
  


# In[ ]:


# Pull in Units
 units = pdf.pq('LTTextLineHorizontal:contains("Units")')
 
 if units.attr('y0') == None:
     x0 = x0 + width1 - 10
     width1 = 60
 
 else:
     x0 = float(units.attr('x0'))-2
     width1 = float(units.attr('width'))
 
 units_orig = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s,%s,%s,%s")' % (x0,y0,x0+width1,y1))
 
 Units = []
 Coords = []
 for d in units_orig.items():
     if d.text() in Results or d.text() in Test:
         continue
     if "Source" in d.text() or "Analysis" in d.text():
         continue
     if "unconfirmed screen" in d.text():
         unconf = True
         continue
     if 'By' in d.text():
         continue
     
     if "Units" not in d.text():
         Units.append(d.text())    
         Coords.append(float(d.attr('y0')))

 Units_df = pd.DataFrame([Units, Coords]).transpose().sort_values(by = 1, ascending=False)
 

