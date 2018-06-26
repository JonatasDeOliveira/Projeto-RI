import json
import os.path
import collections
    
file = './Docs/Jsons/datas.json'

#file = './Indexer/wcipegTeste.json'

#file = './Docs/Jsons/Heuristic2/Specific/Wcipeg/wcipeg.json'
with open(file) as f:
    generalDatas = json.load(f,object_pairs_hook=collections.OrderedDict)
teste =[]
for i in generalDatas["0"]:
    if i == "Problem":
        
        print(i)
