import json
import os.path
import collections
    
file = './Docs/Jsons/datas.json'

#file = './Indexer/wcipegTeste.json'

#file = './Docs/Jsons/Heuristic2/Specific/Wcipeg/wcipeg.json'
with open(file) as f:
    generalDatas = json.load(f)

fixData = {}
for i in range(len(generalDatas["Sites"])):
    uniqueId = 0
    insideData = {}
    for a in generalDatas["Sites"][i]:
        if a == "ID":
            uniqueId = generalDatas["Sites"][i][a]
            print(uniqueId)
        else:
            insideData[a] = generalDatas["Sites"][i][a]
    fixData[uniqueId] = insideData
    
fixData = collections.OrderedDict(sorted(fixData.items()))


file = './Indexer/datasTeste.json'
with open(file, 'w') as f:
    f.write(json.dumps(fixData, indent=2))
