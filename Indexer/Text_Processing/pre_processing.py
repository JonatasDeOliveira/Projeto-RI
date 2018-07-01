from nltk.tokenize import sent_tokenize, word_tokenize #Tokenizer
from nltk.corpus import stopwords #Stopwords
from nltk.stem.porter import * #Porter Stemmer
from Indexer import util
import re

#stopwords
stopWords = set(stopwords.words('english'))
#Stemmer
stemmer = PorterStemmer()

def processData(data):
    #Tokenizer
    wordsList = word_tokenize(data.lower())
    
    
    stopWords = set(stopwords.words('english'))
    wordsFiltered = []
    
    #Filtrando as palavras
    for w in wordsList:
        w = w.encode('ascii','ignore').decode()
        
        resultN = re.match('[0-9]*?\.', w)
        resultT = re.match('[a-z]\.', w)
        if resultN or resultT:
            pass
        #Remove Stopwords
        elif w not in stopWords:
            if re.match('[a-z]*?\.[a-z]*?', w):
                words = w.split('.')
                for i in range(len(words)):
                    if len(words[i]) > 0:
                        wordsFiltered.append(words[i])
            elif len(w) > 0:
                wordsFiltered.append(w)

    words = [stemmer.stem(word) for word in wordsFiltered]
    
    return words
    
def processTimeL(data):
    wordsList = word_tokenize(data.lower())
    
    wordsFiltered = []
    
    for w in wordsList:
        w = w.encode('ascii','ignore').decode()
        
        if re.match('[0-9]*?\.?[0-9]*?s?-', w):
            words = w.split('-')
            for splited in words:
                    wordsList.append(splited)
            continue

        if re.match('[0-9]+?s', w):
            wordsFiltered.append(w.replace('s', ''))
        elif w not in stopWords and len(w) > 0:
            wordsFiltered.append(w)
    
    words = [stemmer.stem(word) for word in wordsFiltered]
    return words