import re
from nltk.tokenize import sent_tokenize, word_tokenize #Tokenizer
from nltk.corpus import stopwords #Stopwords
from nltk.stem.porter import * #Porter Stemmer
import json
import math

input_options = ['Input', 'Input Format', 'Input Description', 'INPUT']
output_options = ['Output', 'Output Format', 'Output Description', 'OUTPUT']
stopWords = set(stopwords.words('english'))
'''
def pre_process(datas, field):
    
    new_data = {}
    for key in datas.keys():
        print('working doc '+key+' - field '+field)
        data = None
        if field == 'Input':
            for input_option in input_options:
                data = datas[key].get(input_option, None)
                if data != None:
                    break
        elif field == 'Output':
            for output_option in output_options:
                data = datas[key].get(output_option, None)
                if data != None:
                    break
        else:
            data = datas[key].get(field, None)
                
        if data == None:
            continue
        
        data = re.compile("\n+").split(data)
        
        for line in data:
            cur_line = line.split(".")
            
            for phrase in cur_line:
                words = word_tokenize(phrase.lower())
                
                for i in range(0,len(words)):
                    if len(words[i]) >= 3 and words[i] not in stopWords:
                        word_dict = new_data.get(words[i],{})
                        length = word_dict.get('count',0)
                        word_dict['count'] = length+1
                        words_bag = word_dict.get('words_bag',{})
                        for j in range(i+1, min((i+5), len(words))):
                            if len(words[j]) >= 3  and words[j] not in stopWords:
                                count_word = words_bag.get(words[j],0)
                                words_bag[words[j]] = count_word+1
                        
                        word_dict['words_bag'] = words_bag
                        new_data[words[i]] = word_dict 

    with open('mutual-information/'+field+'.json', 'w') as outfile:  
        json.dump(new_data, outfile)
    

def load_json(path):
    with open(path) as f:
        data = json.load(f)
    return data

datas = load_json('Docs/Jsons/datas.json')

fields = ['Title','Input','Output','Problem','Description']
for field in fields:
    pre_process(datas,field)
    '''

def load_json(path):
    with open(path) as f:
        data = json.load(f)
    return data

corpus_data = load_json('mutual-information/Corpus.json')
words_number = 0

for key in corpus_data.keys():
    words_number += corpus_data[key]['count']
    
number_docs = 4064.0

def calculate_mutual_info(field):
    
    data = load_json('mutual-information/'+field+'.json')
    mutual_info = {}
    words_cont = 0.0
    for key in data.keys():
        words_cont += data[key]['count']
    
    for key in data.keys():
        
        mutual_info[key] = (float(data[key].get('count'))/words_cont)
        
    with open('mutual-information/calculated/'+field+'.json', 'w') as outfile:  
        json.dump(mutual_info, outfile)


fields = ['Title','Input','Output','Description']

for field in fields:
    calculate_mutual_info(field)