from nltk.tokenize import sent_tokenize, word_tokenize #Tokenizer
from nltk.corpus import stopwords #Stopwords
from nltk.stem.porter import * #Porter Stemmer
import Text_Processing.pre_processing as p
import re
import json
import collections
    #Tokenizer
file = './Indexer/Files/Inverted/nCompressed/Title/title'
with open(file) as f:
    datas = json.load(f, object_pairs_hook=collections.OrderedDict)
    
print(datas["login"])