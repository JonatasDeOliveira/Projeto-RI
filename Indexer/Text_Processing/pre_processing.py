from nltk.tokenize import sent_tokenize, word_tokenize #Tokenizer
from nltk.corpus import stopwords #Stopwords
from nltk.stem.porter import * #Porter Stemmer
import re

def processData(data):
    #Tokenizer
    tokenize = word_tokenize(data.lower())
    
    #Remove stopwords
    stopWords = set(stopwords.words('english'))
    wordsFiltered = []
    
    for w in tokenize:
        w = w.encode('ascii','ignore').decode()
        
        resultN = re.match('[0-9]*?\.', w)
        resultT = re.match('[a-z]\.', w)
        if resultN or resultT:
            pass
        elif w not in stopWords:
            if re.match('[a-z]*?\.[a-z]*?', w):
                words = w.split('.')
                for i in range(len(words)):
                    if len(words[i]) > 0:
                        wordsFiltered.append(words[i])
            elif len(w) > 0:
                wordsFiltered.append(w)
            
            
    #Stemmer
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in wordsFiltered]
    
    return words