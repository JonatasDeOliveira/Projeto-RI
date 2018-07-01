import json
import pickle
import os
import Text_Processing.pre_processing as p
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
num = []
for d in data:
  if re.match("[0-9]*?\.?[0-9]+?", d) is not None:
    num.append(float(d))

numbers = sorted(num)
numbersLen = len(numbers)

q1 = 0.125*numbersLen
q2 = 0.25*numbersLen
q3 = 0.375*numbersLen
q4 = 0.50*numbersLen
q5 = 0.625*numbersLen
q6 = 0.75*numbersLen
q7 = 0.875*numbersLen


print(round(q1))
print(round(q2))
print(round(q3))
print(round(q4))
print(round(q5))
print(round(q6))
print(round(q7))
print("---------------")
print(numbers[round(q1)])
print(numbers[round(q2)])
print(numbers[round(q3)])
print(numbers[round(q4)])
print(numbers[round(q5)])
print(numbers[round(q6)])
print(numbers[round(q7)])

print("---------------")
print (numbers)