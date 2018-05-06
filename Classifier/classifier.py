import json
from sklearn import svm
from sklearn import tree
from stop_words import get_stop_words
import operator
from os.path import isfile, join
import os
from os import listdir
import re

stop_words = get_stop_words('en')

class Classifier:
    def __init__(self):
        self.features = []
        self.features_names = []
        self.clf = self.train()
        
    
    def getIDF(self):
        with open('idf.json') as data_file:    
            data = json.load(data_file)
        return data
    
    
    def setFeatures(self, idf):
        for key in idf.keys():
            self.features_names.append(key)
        
        X, y = self.getTrainData(self.features_names)
    
        clf = tree.DecisionTreeClassifier()
        clf.fit(X, y)
        
        for i in range(0, len(clf.feature_importances_)-1):
            if clf.feature_importances_[i] > 0.000:
                self.features.append(self.features_names[i])
        
    def getTrainData(self, keys):
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
            for key in keys:
                aux.append(data.get(key, 0))
            
            y.append(True)
            X.append(aux)
        
        
        for file in negative_files:
            with open(neg_path+file) as data_file:    
                data = json.load(data_file)
            aux = []
            for key in keys:
                aux.append(data.get(key, 0))
            
            y.append(False)
            X.append(aux)
        yield X
        yield y
        
    def train(self):
        idf = self.getIDF()
        self.setFeatures(idf)
        X, y = self.getTrainData(self.features)
        
        clf = tree.DecisionTreeClassifier()
        clf.fit(X, y)
        
        return clf
        
    def getPageTf(self, page):
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
    
    def classify(self, page):
        tf = self.getPageTf(page)
        
        inst = []
        for feature in self.features:
            inst.append(tf.get(feature, 0))
        
        return self.clf.predict([inst])[0]
        
    
    
    
    