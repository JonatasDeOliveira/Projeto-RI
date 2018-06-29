import json
import pickle
import os

def writeFiles(field, indexes, indexesFrequency, cIndexes, cIndexesFrequency):
    
    os.makedirs('Indexer/Files/Inverted/Compressed/', exist_ok=True)
    os.makedirs('Indexer/Files/Inverted/nCompressed/', exist_ok=True)
    os.makedirs('Indexer/Files/Inverted_Frequency/Compressed/', exist_ok=True)
    os.makedirs('Indexer/Files/Inverted_Frequency/nCompressed/', exist_ok=True)
    
    os.makedirs('Indexer/Files/Pickled/Inverted/Compressed/', exist_ok=True)
    os.makedirs('Indexer/Files/Pickled/Inverted/nCompressed/', exist_ok=True)
    os.makedirs('Indexer/Files/Pickled/Inverted_Frequency/Compressed/', exist_ok=True)
    os.makedirs('Indexer/Files/Pickled/Inverted_Frequency/nCompressed/', exist_ok=True)
    
    #arquivo invertido
    file = './Indexer/Files/Inverted/nCompressed/' + field
    exist = os.path.isfile(file) 
    if not exist:
        with open(file, 'w') as f:
            f.write(json.dumps(indexes, indent=2))
    
    file = './Indexer/Files/Inverted/Compressed/' + field
    with open(file, 'w') as f:
        f.write(json.dumps(cIndexes, indent=2))
    
    #arquivo invertido com frequencia
    file = './Indexer/Files/Inverted_Frequency/nCompressed/' + field
    with open(file, 'w') as f:
        f.write(json.dumps(indexesFrequency, indent=2))

    file = './Indexer/Files/Inverted_Frequency/Compressed/' + field
    with open(file, 'w') as f:
        f.write(json.dumps(cIndexesFrequency, indent=2))
     
       
    #pickled
    file = 'Indexer/Files/Pickled/Inverted/nCompressed/' + field
    out = open(file, 'wb') #writebytes
    pickle.dump(cIndexes, out)
    out.close()
    
    file = 'Indexer/Files/Pickled/Inverted/Compressed/' + field
    out = open(file, 'wb') #writebytes
    pickle.dump(indexes, out)
    out.close()
    
    file = 'Indexer/Files/Pickled/Inverted_Frequency/nCompressed/' + field
    out = open(file, 'wb') #writebytes
    pickle.dump(indexesFrequency, out)
    out.close()

    file = 'Indexer/Files/Pickled/Inverted_Frequency/Compressed/' + field
    out = open(file, 'wb') #writebytes
    pickle.dump(cIndexesFrequency, out)
    out.close()