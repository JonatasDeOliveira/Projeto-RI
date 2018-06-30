import json
import pickle
import os

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