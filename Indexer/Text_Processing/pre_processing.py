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
        result = re.match('[0-9]*?\.', w)
        if not result:
           if w not in stopWords:
            wordsFiltered.append(w)
            
    #Stemmer
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in wordsFiltered]
    print (words)
    return words