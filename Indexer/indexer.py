import json
from Indexer.Text_Processing import pre_processing as p
from Indexer import util

def indexer(datas, field):
    dataLen = len(datas["Sites"])
    
    lField = field.lower()
    
    for n in range(dataLen):
        
        if (field is "Input") or (field is "Output"):
            for f in datas["Sites"][n]:
                if field in f.title():
                    value = datas["Sites"][n][f]
        else:
            value = datas["Sites"][n][field]

        pValue = p.processData(value)
        
        for word in pValue:
            indexes = []
            frequency = 0
            indexesFrequency = []

            #compressed
            cIndexes = []
            cIndexesFrequency = []
    
            for i in range(dataLen):
                text = datas["Sites"][i][field]
                text = text.lower()
                if word in text:
                    pageId = datas["Sites"][i]["ID"]

                    frequency = text.count(word)

                    #Adiciona os valores comprimidos
                    if len(cIndexes) > 0:
                        compressed = pageId - indexes[-1]
                        
                        cIndexes.append(compressed)
                        cIndexesFrequency.append([compressed, frequency])
                    else:
                        cIndexes.append(pageId)
                        cIndexesFrequency.append([pageId, frequency])
                        
                    indexes.append(pageId)
                    indexesFrequency.append([pageId, frequency])
                    
                    
            word = word.replace('/', '-')
            util.writeFile(word, indexes, indexesFrequency, cIndexes, cIndexesFrequency, lField)


file = './Docs/Jsons/Datas.json'
with open(file) as f:
    datas = json.load(f)

indexer(datas, "Title")
"""indexer(datas, "Description")
indexer(datas, "Input")         #Input, Input Descritpion, Input Format, INPUT
indexer(datas, "Output")        #output, Output Descritpion, Output Format, OUTPUT
indexer(datas, "Time Limit")"""

#https://www.youtube.com/watch?v=2Tw39kZIbhs