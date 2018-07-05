import json
from Indexer.Text_Processing import pre_processing as p
from Indexer import util
import collections

indexes = {}

def indexer(datas, field):
    lField = field.lower()
    
    #normal
    indexes = {}
    indexesFrequency = {}

    #compressed
    cIndexes = {}
    cIndexesFrequency = {}
    
    #positional
    posIndexes = {}
    cPosIndexes = {}
    
    for n in datas:
        print("doc - " + n + " field - "+field)
        if (field == "Input") or (field == "Output"):
            for f in datas[n]:
                if field in f.title():
                    text = datas[n][f]
        else:
            text = datas[n][field]
            
        if field == "Time Limit":
            words = p.processTimeL(text)
            
        else:
            words = p.processData(text)
        
        for word in words:
            pageId = int(n)
            
            normalWord = word
            word = word.replace('/', '*')
            
            if field == "Time Limit":
                if util.isNumber(word):
                    word = util.searchRange(util.getRanges(), word)
                    
            if word not in indexes:
                positions = util.getPositions(normalWord, words)
                frequency = len(positions)
                
                indexes[word] = [pageId]
                indexesFrequency[word] = [[pageId, frequency]]
                posIndexes[word] = [[pageId, frequency, positions]]
                
                cIndexes[word] = [pageId]
                cIndexesFrequency[word] = [[pageId, frequency]]
                cPosIndexes[word] = [[pageId, frequency, positions]]
                
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
                    
                    indexes[word].append(pageId)
                    indexesFrequency[word].append([pageId, frequency])
                    posIndexes[word].append([pageId, frequency, positions])
                    
                    cIndexes[word].append(compressedId)
                    cIndexesFrequency[word].append([compressedId, frequency])
                    cPosIndexes[word].append([compressedId, frequency, positions])
                    
                    
    util.writeFiles(lField, indexes, cIndexes, indexesFrequency, cIndexesFrequency, posIndexes, cPosIndexes)
    
def getIndexes(word, indexerType, field):
    if indexerType not in indexes:
        indexes[indexerType] = dowloadIndexes(indexerType, field)
    elif field not in indexes[indexerType]:
        indexes[indexerType].update(dowloadIndexes(indexerType, field))
        
    if word not in indexes[indexerType][field]:
        return []
    else:
        return indexes[indexerType][field][word]

def dowloadIndexes(indexerType, field):
    file = './Indexer/Files/Inverted/' +  indexerType + '/nCompressed/' + field
    with open(file) as f:
        datas = json.load(f)
    return {field : datas}
    
file = './Docs/Jsons/datas.json'
with open(file) as f:
    datas = json.load(f, object_pairs_hook=collections.OrderedDict)


indexer(datas, "Title")
#indexer(datas, "Description")
#indexer(datas, "Input")         #Input, Input Descritpion, Input Format, INPUT
#indexer(datas, "Output")        #output, Output Descritpion, Output Format, OUTPUT
#indexer(datas, "Time Limit")
#indexer(datas, "Problem")



