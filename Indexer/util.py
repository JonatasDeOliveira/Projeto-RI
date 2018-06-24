import json
import pickle
import os

def writeFile(word, indexes, indexesFrequency, cIndexes, cIndexesFrequency, field):
    
    os.makedirs('Indexer/Files/Inverted/Compressed/' + field.title(), exist_ok=True)
    os.makedirs('Indexer/Files/Inverted/nCompressed/' + field.title(), exist_ok=True)
    os.makedirs('Indexer/Files/Inverted_Frequency/Compressed/' + field.title(), exist_ok=True)
    os.makedirs('Indexer/Files/Inverted_Frequency/nCompressed/' + field.title(), exist_ok=True)
    
    file = './Indexer/Files/Inverted/nCompressed/' + field.title() + '/' + word + '.' + field
    exist = os.path.isfile(file) 
    if not exist:
        with open(file, 'w') as f:
            f.write(json.dumps(indexes, indent=2))
        
            
    file = './Indexer/Files/Inverted_Frequency/nCompressed/' + field.title() + '/' + word + '.' + field
    exist = os.path.isfile(file) 
    if not exist:
       with open(file, 'w') as f:
            f.write(json.dumps(indexesFrequency, indent=2))


    file = './Indexer/Files/Inverted/Compressed/' + field.title() + '/' + word + '.' + field
    exist = os.path.isfile(file) 
    if not exist:
        out = open(file, 'wb') #writebytes
        pickle.dump(cIndexes, out)
        out.close()
            
    file = './Indexer/Files/Inverted_Frequency/Compressed/' + field.title() + '/' + word + '.' + field
    exist = os.path.isfile(file) 
    if not exist:
        out = open(file, 'wb') #writebytes
        pickle.dump(cIndexesFrequency, out)
        out.close()