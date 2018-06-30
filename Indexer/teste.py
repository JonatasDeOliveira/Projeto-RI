import json
import pickle
import os
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
"""

data = ['a','ab', 'cd', 'a','25']
print(data)
list(filter(lambda a: a != 2, data))
list(filter(lambda a: a != 'a', data))
print(data)


data = {"aiai": [
    1006,
    1011,
    1029,
    1031,
    1046,
    1047,
    1073,
    1075,
    1082,
    1187
  ]}
  
print (data.values())
if 1006 in data.values():
  print(1006)