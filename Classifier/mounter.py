import re
import urllib.request
from bs4 import BeautifulSoup
import json
from stop_words import get_stop_words
import nltk

stop_words = get_stop_words('en')
ps = nltk.stem.PorterStemmer()

def getPositivePageSpoj(url):
    html = urllib.request.urlopen(url)
    page = BeautifulSoup(html, "html.parser")
    problem = page.find("div", {"id" : "problem-body"})
    title_problem = page.find("h2", {"id" : "problem-name"})
    [s.extract() for s in problem('script')]
    data = ""
    data += (title_problem.get_text())
    data += (problem.get_text())
    
    tf = {}
    regex = r'\b[a-zA-Z]+\b'
    data=re.findall(regex,data)
    
    for word in data:
        if word.lower() not in stop_words:
            tf[word.lower()] = tf.get(word.lower(),0)+1
    
    return tf

def getNegativePageSpoj(url):
    html = urllib.request.urlopen(url)
    page = BeautifulSoup(html, "html.parser")
    [s.extract() for s in page('script')]
   
    data = ""
    data += (page.get_text())
    
    tf = {}
    regex = r'\b[a-zA-Z]+\b'
    data=re.findall(regex,data)
    
    for word in data:
        if word.lower() not in stop_words:
            tf[word.lower()] = tf.get(word.lower(),0)+1
    
    return tf


def getPositiveSpoj(id_doc):
    file = open("positives/links_spoj.txt", "r") 
    links = file.readlines()
    
    idf = {}
    num_pos_docs = 0
    
    for link in links:
        tf = getPositivePageSpoj(link)
        
        num_pos_docs+=1
        for key in tf.keys():
            idf[key] = 1+idf.get(key,0)
        
        with open("positive_docs/"+str(id_doc)+'.json', 'w') as fp:
            json.dump(tf, fp)
        id_doc+=1
    #idf só está pegando a frequência de cada palavra nos documentos
    print(idf)

def getNegativeSpoj(id_doc):
    file = open("negatives/links_spoj.txt", "r") 
    links = file.readlines()
     
    
    for link in links:
        tf = getNegativePageSpoj(link)
        
        with open("negative_docs/"+str(id_doc)+'.json', 'w') as fp:
            json.dump(tf, fp)
        id_doc+=1
        




id_doc = 1001

getPositiveSpoj(id_doc)

getNegativeSpoj(id_doc)



#IDF(t) = log_e(Total number of documents / Number of documents with term t in it).