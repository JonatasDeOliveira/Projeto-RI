import bs4 as bs
import requests
from Extractor import util

def dmoj(page, link, uniqueId): 
    #request = requests.get("https://dmoj.ca/problem/ccc13j3")
    #page = bs.BeautifulSoup(request.content, "html.parser")
    
    title = page.title
    title = title.text
    problemName = title.replace(" - DMOJ: Modern Online Judge", "")
    
    problem = page.find("div", {"class": "content-description screen"})
    problemBody = problem.div
    problemBodyText = problemBody.text
    
    bodyArray = problemBodyText.split("\n")
    
    startIndex = 0
    inputIndex = -1
    outputIndex = -1
    sampleIndex = -1
    notesIndex = -1
    constraintsIndex = -1
    timeLimitIndex = -1
    endIndex = len(bodyArray)
    
    for i in range(endIndex):
        #Input Desc
        if bodyArray[i] == "Input Specification":
            inputIndex = i
        elif bodyArray[i] == "Input":
            bodyArray[i] = "Input Specification"
            inputIndex = i
        #Output Desc
        if bodyArray[i] == "Output Specification":
            outputIndex = i
        elif bodyArray[i] == "Output":
            bodyArray[i] = "Output Specification"
            outputIndex = i
        #Examples Desc
        if sampleIndex != -1:
            sampleIndex = sampleIndex
        elif "Sample Input" in bodyArray[i]:
            sampleIndex = i
        #Notes
        if bodyArray[i] == "Note":
            notesIndex = i
        #Constraints
        if "Constraints" in bodyArray[i]:
            constraintsIndex = i
    
    indexes = [startIndex, inputIndex, outputIndex, sampleIndex, notesIndex, constraintsIndex, endIndex, timeLimitIndex]
    indexes.sort()
    dataT = {}
    
    for i in range(len(indexes)):
        if indexes[i] == -1:
            continue
        if (i+1) == (len(indexes)):
            continue
        if indexes[i] == 0:
            dataT["Description"] = util.getTextInfo(bodyArray, indexes[i], indexes[i+1])
        elif sampleIndex == indexes[i]:
            dataT["Example"] = util.getTextInfo(bodyArray, indexes[i], indexes[i+1])
        else:
            info = util.getTextInfo(bodyArray, indexes[i], indexes[i+1])
            info = info.replace(bodyArray[indexes[i]] + "\n", "")
            dataT[bodyArray[indexes[i]]] = info
    
    limits = page.findAll("div", {"class": "problem-info-entry"})
    problemTime = ""
    problemMemory = ""
    if (len(limits) >= 3):
        problemTime = limits[1].text[1:-1]
        problemMemory = limits[2].text[1:-1]
    
    dataT["Title"] = problemName
    dataT["Time Limit"] = problemTime.replace("Time limit:\n", "")
    dataT["Memory Limit"] = problemMemory.replace("Memory limit:\n", "")
    
    title = page.find("div", {"class" : "problem-title"})
    
    limit = ""
    for lim in limits:
        limit += lim.text + "\n"
    
    dataT["Problem"] = title.text + "\n" + util.getText(problem) + "\n" + limit[:-1]
    dataT["URL"] = link
    
    data = {}
    data[uniqueId] = dataT
    
    util.loadData(data)