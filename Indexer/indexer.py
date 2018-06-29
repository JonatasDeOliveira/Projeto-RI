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
    
    for n in datas:
        if (field is "Input") or (field is "Output"):
            for f in datas[n]:
                if field in f.title():
                    value = datas[n][f]
        else:
            value = datas[n][field]
            
        pValue = p.processData(value)
        
        for word in pValue:
            pageId = int(n)
            
            word = word.replace('/', '*')
            
            if word not in indexes.keys():
                indexes[word] = [pageId]
                indexesFrequency[word] = [[pageId, 1]]
                    
                cIndexes[word] = [pageId]
                cIndexesFrequency[word] = [[pageId, 1]]
            else:
                indexList = indexes[word]
                compressedId = pageId - indexList[-1]
                
                frequency = 0
                indexesLen = len(indexes[word])
                for i in range(indexesLen):
                    index = indexesFrequency[word][i]
                    if index[0] == pageId:
                        frequency = 1 + index[1]
                        
                        indexesFrequency[word][i][1] = frequency
                        cIndexesFrequency[word][i][1] = frequency
                
                if frequency == 0:
                    indexes[word].append(pageId)
                    indexesFrequency[word].append([pageId, 1])
                    
                    cIndexes[word].append(compressedId)
                    cIndexesFrequency[word].append([compressedId, 1])
    util.writeFiles(lField, indexes, indexesFrequency, cIndexes, cIndexesFrequency)


file = './Docs/Jsons/datas.json'
with open(file) as f:
    datas = json.load(f, object_pairs_hook=collections.OrderedDict)

indexer(datas, "Title")
"""
indexer(datas, "Description")
indexer(datas, "Input")         #Input, Input Descritpion, Input Format, INPUT
indexer(datas, "Output")        #output, Output Descritpion, Output Format, OUTPUT
indexer(datas, "Time Limit")"""