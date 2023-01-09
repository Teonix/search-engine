# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 12:56:22 2020

@author: Teonix
"""

import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID

#Δημιουργία συνάρτησης για τη πραγματοποίηση του indexing
def createSearchableData(root): 
    #Ορισμός των περιεχομένων(fields) του Index 
    schema = Schema(title=TEXT(stored=True),path=ID(stored=True),\
              content=TEXT,textdata=TEXT(stored=True))
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
    #Δημιουργία του Index
    ix = create_in("indexdir",schema)
    writer = ix.writer()

    #Διαδικασία indexing των αρχείων που δώσαμε στο αντίστοιχο path
    filepaths = [os.path.join(root,i) for i in os.listdir(root)]
    for path in filepaths:
        fp = open(path,'r')
        print(path)
        text = fp.read()
        writer.add_document(title=path.split("\\")[1], path=path,\
          content=text,textdata=text)
        fp.close()
    writer.commit()
 
root = ""

#Κάλεσμα της συνάρτησης που κάνει indexing, τοποθετώντας το path με τα files
createSearchableData(root)

from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import open_dir
from whoosh.query import *
from whoosh.qparser import QueryParser

ix = open_dir("indexdir")
searcher = ix.searcher()
#Ο χρήστης δίνει το query
myquery = input("Enter query:")

#Διαδικασία πραγματοποίησης searching
with ix.searcher(weighting=scoring.Frequency) as searcher:
    qp = QueryParser("content", ix.schema)
    q = qp.parse(myquery)
    results = searcher.search(q,limit=None)
    #Παρουσίαση αποτελεσμάτων
    print("\n")
    print("The Results: \n")
    print(results)
    for i in range(len(results)):
       print("Score:", str(results[i].score), " ", "Content:", results[i]['textdata'], " ", "Path:", results[i]['path'])

