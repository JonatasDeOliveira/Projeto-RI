import json
import pickle
import os

indexesData = {}
indexesFrequencyData = {}
cIndexesData = {}
cIndexesFrequencyData = {}

def loadData(word, indexes, indexesFrequency, cIndexes, cIndexesFrequency):
    indexesData.update({word : indexes})
    indexesFrequencyData.update({word : indexesFrequency})
    cIndexesData.update({word : cIndexes})
    cIndexesFrequencyData.update({word : cIndexesFrequency})


def writeFiles(field):
    
    os.makedirs('Indexer/Files/Inverted/Compressed/' + field.title(), exist_ok=True)
    os.makedirs('Indexer/Files/Inverted/nCompressed/' + field.title(), exist_ok=True)
    os.makedirs('Indexer/Files/Inverted_Frequency/Compressed/' + field.title(), exist_ok=True)
    os.makedirs('Indexer/Files/Inverted_Frequency/nCompressed/' + field.title(), exist_ok=True)
    
    #arquivo invertido
    file = './Indexer/Files/Inverted/nCompressed/' + field.title() + '/' + field
    exist = os.path.isfile(file) 
    if not exist:
        with open(file, 'w') as f:
            f.write(json.dumps(indexesData, indent=2))
    
    file = './Indexer/Files/Inverted/Compressed/' + field.title() + '/' + field
    exist = os.path.isfile(file) 
    if not exist:
        with open(file, 'w') as f:
            f.write(json.dumps(cIndexesData, indent=2))
    
    #arquivo invertido com frequencia
    file = './Indexer/Files/Inverted_Frequency/nCompressed/' + field.title() + '/' + field
    exist = os.path.isfile(file) 
    if not exist:
       with open(file, 'w') as f:
            f.write(json.dumps(indexesFrequencyData, indent=2))

    file = './Indexer/Files/Inverted_Frequency/Compressed/' + field.title() + '/' + field
    exist = os.path.isfile(file) 
    if not exist:
        with open(file, 'w') as f:
            f.write(json.dumps(cIndexesFrequencyData, indent=2))
        
    """
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
        
        """