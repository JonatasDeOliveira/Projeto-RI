import bs4 as bs
import re
import math
import json
import os.path
import collections
import os

datas = {}

def treatStr(sample):
    samples = re.findall('\>.*?\<',str(sample))
    sampleStr = ""
    for s in samples:
        if len(s) > 2:
            sampleStr += s[1:-1] + "\n"
    return sampleStr[:-1]
    
def findIndex(array, string):
    for i in range(0, len(array)):
        text = array[i].text
        if string in text:
            return i
  
def findTextIndex(array, string):
     for i in range(0, len(array)):
        if string == array[i]:
            return i

def getInfo(array, s, e):
    info = ""
    for i in range(s, e):
        info += array[i].text + "\n"
    return info

def getTextInfo(array, s, e):
    info = ""
    for i in range(s, e):
        info += array[i] + "\n"
    return info
   
def getEvenText(array):
    even = ""
    for i in range(len(array)):
        if math.fmod(i, 2) == 0:
            even += array[i].text + "\n\n"
    return even 

def getOddText(array):
    odd = ""
    for i in range(len(array)):
        if math.fmod(i, 2) == 1:
            odd += array[i].text + "\n\n"
    return odd[:-2]

def findBetween(s, firstS, lastS ):
    start = s.index(firstS) + len(firstS)
    end = s.index(lastS, start)
    return str(s[start:end])
    
def checkMap(mapList, keyT):
    for key in mapList:
        if key == keyT:
            return True
    return False

def getMaxKey(mapList):
    maxKey = ""
    maxValue = 0
    for key in mapList:
        if maxValue < mapList[key]:
            maxValue = mapList[key]
            maxKey = key
    return maxKey

def loadData(data):
    datas.update(data)

def writeJSON(crawlerType, extractorType, domain, fileName):
    #datas = collections.OrderedDict(sorted(datas.items()))
    #Escrever em um JSON para o especifico
    #file = './Docs/Jsons/' + crawlerType + '/'+ extractorType + '/' + domain + '/' + fileName + '.json'
    file = './Extrator/json' + crawlerType + '/'+ extractorType + '/' + domain + '/' + fileName + '.json'
    os.makedirs('./Extrator/json' + crawlerType + '/'+ extractorType + '/' + domain + '/' , exist_ok=True)
    print("oi")
    with open(file, 'w') as f:
            f.write(json.dumps(datas, indent=2))
    
    """
    #Escreve em um JSON tudo
    file = './Docs/Jsons/datas.json'
    with open(file) as f:
        generalDatas = json.load(f)
    
    generalDatas.update(datas)
    
    generalDatas = collections.OrderedDict(sorted(generalDatas.items()))
    with open(file, 'w') as f:
        f.write(json.dumps(generalDatas, indent=2))
    """
def getText(page):
    [s.extract() for s in page.findAll(['style', 'script'])]
    return page.text