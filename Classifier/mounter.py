import re
import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup
import json
from stop_words import get_stop_words
import nltk
import operator
import signal
import math
import os
from os import listdir
from os.path import isfile, join
from sklearn import tree
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier


stop_words = get_stop_words('en')
ps = nltk.stem.PorterStemmer()
idf = {}

def getTFFromPage(url):
    '''
    driver = webdriver.PhantomJS( service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
    driver.get(url)
    page = BeautifulSoup(driver.page_source, "html.parser")
    driver.service.process.send_signal(signal.SIGTERM)
    '''
    html = urllib.request.urlopen(url)
    page = BeautifulSoup(html, "html.parser")
    
    
    [s.extract() for s in page('script')]
    data = ""
    data += (page.get_text())
    
    tf = {}
    regex = r'\b[a-zA-Z]+\b'
    data=re.sub("[^\w]", " ",  data).split()
    
    for word in data:
        if word.lower() not in stop_words and len(word)>2:
            tf[word.lower()] = tf.get(word.lower(),0)+1
    
    return tf


def positiveTF(id_doc):
    global idf
    file = open("positives/links_spoj.txt", "r") 
    links = file.readlines()
    
    num_pos_docs = 0
    
    for link in links:
        if link != "\n":
            tf = getTFFromPage(link)
            num_pos_docs+=1
            for key in tf.keys():
                idf[key] = 1+idf.get(key,0)
        
            with open("positive_docs/"+str(id_doc)+'.json', 'w') as fp:
                json.dump(tf, fp)
            id_doc+=1
            

def negativeTF(id_doc):
    global idf
    file = open("negatives/links_spoj.txt", "r") 
    links = file.readlines()
    
    num_pos_docs = 0
    
    for link in links:
        if link != "\n":
            tf = getTFFromPage(link)
            num_pos_docs+=1
            for key in tf.keys():
                idf[key] = 1+idf.get(key,0)
        
            with open("negative_docs/"+str(id_doc)+'.json', 'w') as fp:
                json.dump(tf, fp)
            id_doc+=1
            
def generateTF():
    id_doc = 1001
    global idf
    
    positiveTF(id_doc)
    negativeTF(id_doc)
    
    length_pos_docs = countFiles("positive_docs")
    length_neg_docs = countFiles("negative_docs")
    #idf calculo
    for key in idf.keys():
        idf[key] = math.log((length_neg_docs+length_pos_docs)/idf.get(key))
    
    with open('idf.json', 'w') as fp:
        json.dump(idf, fp)
    

def getIDF():
    global idf
    if os.path.exists("idf.json"):
        with open('idf.json') as data_file:    
            data = json.load(data_file)
        return data
    else:
        return idf
        
    
def countFiles(path):
    path, dirs, files = next(os.walk(path))
    return len(files)

def classify():
    
    #generateTF()
        
    length_pos_docs = countFiles("positive_docs")
    length_neg_docs = countFiles("negative_docs")
    
    idf = getIDF()
    
    #idf só está pegando a frequência de cada palavra nos documentos
    idf_sorted = sorted(idf.items(), key=operator.itemgetter(1))
    
    #pegando as 100 primeiras features que não aparecem em todos os documentos, que tem o idf maior que 0 
    cont = 0
    features = []
    for x in idf_sorted:
        if x[1] > 0 and cont < 100:
            features.append(x[0])
            cont+=1
    
    pos_path = "positive_docs/"
    neg_path = "negative_docs/"
    positive_files = [f for f in listdir(pos_path) if isfile(join(pos_path, f))]
    negative_files = [f for f in listdir(neg_path) if isfile(join(neg_path, f))]
    
    X = []
    y = []
    for file in positive_files:
        with open(pos_path+file) as data_file:    
            data = json.load(data_file)
        aux = []
        for feature in features:
            aux.append(data.get(feature, 0))
        
        y.append('positive')
        X.append(aux)
    
    
    for file in negative_files:
        with open(neg_path+file) as data_file:    
            data = json.load(data_file)
        aux = []
        for feature in features:
            aux.append(data.get(feature, 0))
        
        y.append('negative')
        X.append(aux)
    
    skf = StratifiedKFold(n_splits=10)
    sets = skf.split(X, y)
    
    accuracy = 0.0
    got_right = 0.0
    got_wrong = 0.0
    count = 0
    
    for train_indexes, test_indexes in sets:
        train_set_inst = []
        train_set_clas = []
        for i in train_indexes:
            train_set_inst.append(X[i])
            train_set_clas.append(y[i])
        
        for i in test_indexes:
            prediction = classifyKNN(train_set_inst, train_set_clas, X[i])
            if prediction == y[i]:
                got_right += 1
            else:
                got_wrong += 1
        accuracy += got_right/(got_right+got_wrong)
        count+=1
    accuracy /= count
    print("accuracy = ", accuracy, "%")
    #print(y)
    #print(features)


def classifyDecisionTree(train_set_inst, train_set_clas, x):
            
    clf = tree.DecisionTreeClassifier()
    clf.fit(train_set_inst, train_set_clas)
    
    print(clf.feature_importances_)
    return clf.predict([x])
        
    
def classifyNaiveBayes(train_set_inst, train_set_clas, x):
    gnb = MultinomialNB()
    gnb.fit(train_set_inst, train_set_clas)
    
    return gnb.predict([x])

def classifySVM(train_set_inst, train_set_clas, x):
    clf = svm.SVC()
    clf.fit(train_set_inst, train_set_clas)
    
    return clf.predict([x])
    
def classifyMLP(train_set_inst, train_set_clas, x):
    clf = MLPClassifier()
    clf.fit(train_set_inst, train_set_clas)
    
    return clf.predict([x])

def classifyKNN(train_set_inst, train_set_clas, x):
    knn = KNeighborsClassifier(n_neighbors=1, weights='distance')
    knn.fit(train_set_inst, train_set_clas)
    
    return knn.predict([x])

classify()