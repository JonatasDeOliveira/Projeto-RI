import json
import pickle
import os
import re

def getPositions(word, words):
    positions = []
    
    lenList = len(words)
    for index in range(lenList):
        if words[index] == word:
            positions.append(index)
    
    return positions

def writeFiles(field, indexes, indexesFrequency, cIndexes, cIndexesFrequency, posIndexes):
    
    os.makedirs('Indexer/Files/Inverted/Basic/Compressed/', exist_ok=True)
    os.makedirs('Indexer/Files/Inverted/Basic/nCompressed/', exist_ok=True)
    os.makedirs('Indexer/Files/Inverted/Positional/', exist_ok=True)
    os.makedirs('Indexer/Files/Inverted/Frequency/Compressed/', exist_ok=True)
    os.makedirs('Indexer/Files/Inverted/Frequency/nCompressed/', exist_ok=True)
    
    os.makedirs('Indexer/Files/Pickled/Inverted/Basic/Compressed/', exist_ok=True)
    os.makedirs('Indexer/Files/Pickled/Inverted/Basic/nCompressed/', exist_ok=True)
    os.makedirs('Indexer/Files/Pickled/Inverted/Positional/', exist_ok=True)
    os.makedirs('Indexer/Files/Pickled/Inverted/Frequency/Compressed/', exist_ok=True)
    os.makedirs('Indexer/Files/Pickled/Inverted/Frequency/nCompressed/', exist_ok=True)

    #arquivo invertido
    file = './Indexer/Files/Inverted/Basic/nCompressed/' + field
    with open(file, 'w') as f:
        f.write(json.dumps(indexes, indent=2))
    
    file = './Indexer/Files/Inverted/Basic/Compressed/' + field
    with open(file, 'w') as f:
        f.write(json.dumps(cIndexes, indent=2))
    
    #arquivo invertido posicional
    file = './Indexer/Files/Inverted/Positional/' + field
    with open(file, 'w') as f:
        f.write(json.dumps(posIndexes, indent=2))
    
    #arquivo invertido com frequencia
    file = './Indexer/Files/Inverted/Frequency/nCompressed/' + field
    with open(file, 'w') as f:
        f.write(json.dumps(indexesFrequency, indent=2))

    file = './Indexer/Files/Inverted/Frequency/Compressed/' + field
    with open(file, 'w') as f:
        f.write(json.dumps(cIndexesFrequency, indent=2))
       
    #pickled
    file = './Indexer/Files/Pickled/Inverted/Basic/nCompressed/' + field
    out = open(file, 'wb') #writebytes
    pickle.dump(cIndexes, out)
    out.close()
    
    file = './Indexer/Files/Pickled/Inverted/Basic/Compressed/' + field
    out = open(file, 'wb') 
    pickle.dump(indexes, out)
    out.close()
    
    file = './Indexer/Files/Pickled/Inverted/Positional/' + field
    out = open(file, 'wb') 
    pickle.dump(posIndexes, out)
    out.close()
    
    file = './Indexer/Files/Pickled/Inverted/Frequency/nCompressed/' + field
    out = open(file, 'wb')
    pickle.dump(indexesFrequency, out)
    out.close()

    file = './Indexer/Files/Pickled/Inverted/Frequency/Compressed/' + field
    out = open(file, 'wb')
    pickle.dump(cIndexesFrequency, out)
    out.close()
    

def isNumber(string):
    return re.match("[0-9]*?\.?[0-9]+?", string) is not None
    
def octil(data):
    #get numbers from data
    numbers = []
    for n in data:
        if isNumber(n):
            if float(n) not in numbers:
                numbers.append(float(n))

    numbers = sorted(numbers)
    numbersLen = len(numbers)
    
    o0 = 0
    o1 = 0.125*numbersLen
    o2 = 0.25*numbersLen
    o3 = 0.375*numbersLen
    o4 = 0.50*numbersLen
    o5 = 0.625*numbersLen
    o6 = 0.75*numbersLen
    o7 = 0.875*numbersLen
    o8 = numbersLen - 1
    
    return [str(numbers[round(o0)])+ "-" + str(numbers[round(o1)]),
            str(numbers[round(o1)])+ "-" + str(numbers[round(o2)]),
            str(numbers[round(o2)])+ "-" + str(numbers[round(o3)]),
            str(numbers[round(o3)])+ "-" + str(numbers[round(o4)]),
            str(numbers[round(o4)])+ "-" + str(numbers[round(o5)]),
            str(numbers[round(o5)])+ "-" + str(numbers[round(o6)]),
            str(numbers[round(o6)])+ "-" + str(numbers[round(o7)]),
            str(numbers[round(o7)])+ "-" + str(numbers[round(o8)])]

def searchOctil(oc, num):
    for o in oc:
        values = o.split('-')
        if isNumber(values[0]):
            if float(num) >= float(values[0]) and float(num) < (float(values[1]) + 0.1):
                return o