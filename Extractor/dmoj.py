import bs4 as bs
import requests
import util

def dmoj(page, crawlerType, extractorType, domain, fileName): 
    #request = requests.get("https://dmoj.ca/problem/ccc13j3")
    #page = bs.BeautifulSoup(request.content, "html.parser")
    
    problemHead = page.find("div", {"class": "problem-title"})
    problemName = problemHead.h2.text
    
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
    data = {}
    
    for i in range(len(indexes)):
        if indexes[i] == -1:
            continue
        if (i+1) == (len(indexes)):
            continue
        if indexes[i] == 0:
            data["Description"] = util.getTextInfo(bodyArray, indexes[i], indexes[i+1])
        elif sampleIndex == indexes[i]:
            data["Example"] = util.getTextInfo(bodyArray, indexes[i], indexes[i+1])
        else:
            info = util.getTextInfo(bodyArray, indexes[i], indexes[i+1])
            info = info.replace(bodyArray[indexes[i]] + "\n", "")
            data[bodyArray[indexes[i]]] = info
    
    limits = page.findAll("div", {"class": "problem-info-entry"})
    
    problemTime = limits[1].text[1:-1]
    problemMemory = limits[2].text[1:-1]
    
    data["Ttile"] = problemName
    data["Time Limit"] = problemTime.replace("Time limit:\n", "")
    data["Memory Limit"] = problemMemory.replace("Memory limit:\n", "")
    
    util.writeToJSON(crawlerType, extractorType, domain, fileName, data)