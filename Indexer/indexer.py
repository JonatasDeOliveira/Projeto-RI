import json
from Indexer.Text_Processing import pre_processing as p
from Indexer import util
import collections

def indexer(datas, field):
    lField = field.lower()
    
    indexes = {}
    indexesFrequency = {}

    #compressed
    cIndexes = {}
    cIndexesFrequency = {}
    
    #Positional
    posIndexes = {}
    
    for n in datas:
        if (field is "Input") or (field is "Output"):
            for f in datas[n]:
                if field in f.title():
                    text = datas[n][f]
        else:
            text = datas[n][field]
            
        words = p.processData(text)
        
        for word in words:
            pageId = int(n)
            
            normalWord = word
            word = word.replace('/', '*')
             
            if word not in indexes:
                positions = util.getPositions(normalWord, words)
                frequency = len(positions)
                
                #indice invertido 
                indexes[word] = [pageId]
                indexesFrequency[word] = [[pageId, frequency]]

                #indice invertido com compressão
                cIndexes[word] = [pageId]
                cIndexesFrequency[word] = [[pageId, frequency]]
                
                #indice invertido posicional
                posIndexes[word] = [[pageId, frequency, positions]]
                
            else:
                compressedId = pageId - indexes[word][-1]
                
                indexesLen = len(indexes[word])
                
                #Vendo se o id já está adicionado, pois como podem existir palavras 
                #repetidas no texto e elas ja foram adicionadas, não pode duplicar valores
                exists = False
                for i in range(indexesLen):
                    value = indexes[word][i]
                    if value == pageId:
                        exists = True
                
                if not exists:
                    positions = util.getPositions(normalWord, words)
                    frequency = len(positions)
                    
                    #indice invertido 
                    indexes[word].append(pageId)
                    indexesFrequency[word].append([pageId, frequency])
    
                    #indice invertido com compressão
                    cIndexes[word].append(compressedId)
                    cIndexesFrequency[word].append([compressedId, frequency])
                    
                    #indice invertido posicional
                    posIndexes[word].append([pageId, frequency, positions])
                    
    util.writeFiles(lField, indexes, indexesFrequency, cIndexes, cIndexesFrequency, posIndexes)


file = './Docs/Jsons/datas.json'
with open(file) as f:
    datas = json.load(f, object_pairs_hook=collections.OrderedDict)

#indexer(datas, "Title")
#indexer(datas, "Description")
#indexer(datas, "Input")         #Input, Input Descritpion, Input Format, INPUT
indexer(datas, "Output")        #output, Output Descritpion, Output Format, OUTPUT
#indexer(datas, "Time Limit")