import json
import pickle
import os
import re
"""
file = './Indexer/t1P'
out = open(file, 'wb') #writebytes
pickle.dump({
  "pickle-jar": [
    98,2
  ],
  "pi": [
    98,2
  ]
 }, out)
out.close()

file = './Indexer/t1.1P'
out = open(file, 'wb') #writebytes
pickle.dump({
  "pickle-jar": 0b1110001010000010,
  "pi": 0b1110001010000010
  
 }, out)
out.close()

file = './Indexer/Files/Inverted/Basic/nCompressed/time limit'
with open(file) as f:  
    data = json.load(f)

for d in p.processTitle(data):
  print (d)
  print("-----------")
  
print(p.processData("3s"))

file = './Docs/Jsons/datas.json'
with open(file) as f:
    datas = json.load(f)
    
for d in datas:
  print(datas[d]["Time Limit"])
  print("-------------------------")
"""
"""
data = [2,3,4,5]

for d in data:
  if d == 2:
    data.append(6)
  print (d)
  
"""

file = './Indexer/Files/Inverted/Basic/nCompressed/time limit'
with open(file) as f:  
    data = json.load(f)

print(data)
