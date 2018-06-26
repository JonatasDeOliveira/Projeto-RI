import json
from Indexer.Text_Processing import pre_processing as p
from Indexer import util
import collections

def indexer(datas, field):
    lField = field.lower()
    
    for n in datas:
        if (field is "Input") or (field is "Output"):
            for f in datas[n]:
                if field in f.title():
                    value = datas[n][f]
        else:
            value = datas[n][field]

        pValue = p.processData(value)
        
        for word in pValue:
            indexes = []
            frequency = 0
            indexesFrequency = []

            #compressed
            cIndexes = []
            cIndexesFrequency = []
    
            for i in datas:
                
                #acha o verdadeiro atributo para pesquisa posterior
                actualField = field
                if (field is "Input") or (field is "Output"):
                    for f in datas[n]:
                        print(f)
                        if field in f.title():
                            actualField = f
                            
                text = datas[i][actualField]
                text = text.lower()
                if word in text:
                    pageId = int(i)

                    frequency = text.count(word)

                    #Adiciona os valores comprimidos
                    if len(cIndexes) > 0:
                        
                        compressed = pageId - indexes[-1]
                        print(pageId)
                        print( " - " )
                        print(indexes[-1])
                        print(" = ")
                        print(compressed)
                        cIndexes.append(compressed)
                        cIndexesFrequency.append([compressed, frequency])
                    else:
                        cIndexes.append(pageId)
                        cIndexesFrequency.append([pageId, frequency])
                        
                    indexes.append(pageId)
                    indexesFrequency.append([pageId, frequency])
                    
                    
            word = word.replace('/', '*')
            util.loadData(word, indexes, indexesFrequency, cIndexes, cIndexesFrequency)
    util.writeFiles(lField)


file = './Docs/Jsons/datas.json'
with open(file) as f:
    datas = json.load(f, object_pairs_hook=collections.OrderedDict)

indexer(datas, "Title")
"""indexer(datas, "Description")
indexer(datas, "Input")         #Input, Input Descritpion, Input Format, INPUT
indexer(datas, "Output")        #output, Output Descritpion, Output Format, OUTPUT
indexer(datas, "Time Limit")"""

#https://www.youtube.com/watch?v=2Tw39kZIbhs