import math
import json
import pickle

def codefy(n):
    number = format(n, '08b')
    if n > 0:
        log2 = math.log(n, 2.0)
        numberLen = math.ceil(log2)
    else: 
        numberLen = 0
        
    arrayBytes = []
    bytesStr = []
    
    iterations = math.ceil(numberLen/7)
    arraylen = iterations
    lowerIndex = numberLen - 7
    higherIndex = numberLen
    
    if numberLen > 7:
        while(iterations > 0):
            n = number[lowerIndex : higherIndex]
            bytesStr.append(format(int(str(n),2),'07b'))
            
            higherIndex -= 7
            lowerIndex -= 7
            if lowerIndex < 0:
                lowerIndex = 0
            iterations -= 1
            
        for i in range(arraylen):
            arrayBytes.append(int(str(bytesStr[i]), 2))
        arrayBytes[0] = int('1' + str(bytesStr[0]), 2)
        
    else:
        arrayBytes.append(int('1' + str(number)[1:],2))
    return list(reversed(arrayBytes))

def encodeData(array):
    encodedData = []
    for n in array:
        if type(n) == list:
            encodedData.extend(encodeData(n))
        else:
            encodedData.extend(codefy(n))
    return encodedData
    
def encoder(data):
    indexes = {}
    
    for word in data:
        encodedData = []
        encodedData.extend(encodeData(data[word]))
        indexes[word] = bytes(encodedData)
    return indexes