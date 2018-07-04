import json
import pickle
import os
import re
from Indexer.Variant_Size import encode

folds = ['Inverted/', 'Variant/', 'Pickled/']

def getPositions(word, words):
    positions = []
    
    lenList = len(words)
    for index in range(lenList):
        if words[index] == word:
            positions.append(index)
    
    return positions

def writeFile(field, indexType, fileType, data):
    for fold in folds:
        path = 'Indexer/Files/' + fold + indexType + fileType
        os.makedirs(path, exist_ok=True)
        
        if 'Inverted' in fold:
            with open(path + field, 'w') as f:
                 f.write(json.dumps(data))
        else:
            if 'Variant' in fold:
                newData = encode.encoder(data)
            else:
                newData = data
            with open(path + field, 'wb') as f:
                pickle.dump(newData, f)

def writeFiles(field, indexes, cIndexes, indexesFrequency, cIndexesFrequency, posIndexes, cPosIndexes):
    
    writeFile(field, 'Basic/', 'nCompressed/', indexes)
    writeFile(field, 'Basic/', 'Compressed/', cIndexes)
    
    writeFile(field, 'Frequency/', 'nCompressed/', indexesFrequency)
    writeFile(field, 'Frequency/', 'Compressed/', cIndexesFrequency)
    
    writeFile(field, 'Positional/', 'nCompressed/', posIndexes)
    writeFile(field, 'Positional/', 'Compressed/', cPosIndexes)

def searchRange(ranges, num):
    for r in ranges:
        values = r.split('-')
        if isNumber(values[0]):
            if (values[1] == "") and (float(num) >= float(values[0])):
                return r
            elif (float(num) >= float(values[0])) and (float(num) < (float(values[1]))):
                return r
    

def getRanges():
    return ['0-0.5', '0.5-1', '1-2', '2-3', '3-4', '4-5',
            '5-6', '6-7', '7-8', '8-9', '9-10', '10-15', 
            '15-20', '20-30', '30-']
    
def isNumber(string):
    return re.match("[0-9]*?\.?[0-9]+?", string) is not None
    