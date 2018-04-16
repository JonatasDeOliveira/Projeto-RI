import bs4 as bs
import re
import math

def treatStr(sample):
    samples = re.findall('\>.*?\<',str(sample))
    sampleStr = ""
    for s in samples:
        if len(s) > 2:
            newS = s.replace(">", "")
            newS = newS.replace("<", "")
            sampleStr += newS + "\n"
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
    

def getDatas(datas, arrayInfo, tag):
    text = ""
    for info in arrayInfo[1:]:
        if info.name == tag:
            datas.append(text[:-1])
            text = info.text + "\n"
        else:
            text += info.text + "\n"
    datas.append(text[:-1])
    return datas