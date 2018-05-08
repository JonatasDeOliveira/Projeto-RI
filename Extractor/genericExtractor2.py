from bs4 import BeautifulSoup
import requests
import util
from selenium import webdriver
import signal

def genericExtractor2(page, crawlerType, extractorType, domain, fileName):
    #request = requests.get("https://dmoj.ca/problem/ccc96s1", verify = False)
    #page = BeautifulSoup(request.content, "html.parser")
    
    #driver = webdriver.PhantomJS()
    #driver.get("http://www.spoj.com/problems/TTABLE/")
    #page = BeautifulSoup(driver.page_source, "html.parser")
    #driver.service.process.send_signal(signal.SIGTERM)
    
    mapList = {}
    
    def walker(soup):
        if soup.name is not None:
            for child in soup.children:
                count = 0
                if "Input" in (str(child)):
                    count += 1
                if "Output" in (str(child)):
                    count += 1
                if "Example" in (str(child)):
                    count += 1
                if "Sample" in (str(child)):
                    count += 1
                if "Note" in (str(child)):
                    count += 1
                if "Constraint" in (str(child)):
                    count += 1
                if "Follow up" in (str(child)):
                    count += 1
                if "time limit" in (str(child)).lower():
                    count += 1
                if "memory limit" in (str(child)).lower():
                    count += 1
                
                if util.checkMap(mapList, str(child.parent)):
                    mapList[str(child.parent)] = count + mapList[str(child.parent)]
                else:
                    mapList[str(child.parent)] = count
                walker(child)
                
    walker(page)
    body = BeautifulSoup(util.getMaxKey(mapList), "html.parser")
    bodyArray = body.text.split("\n")
    
    startIndex = 0
    inputIndex = -1
    outputIndex = -1
    sampleIndex = -1
    notesIndex = -1
    constraintsIndex = -1
    followupIndex = -1
    timeLimitIndex = -1
    memoryLimitIndex = -1
    endIndex = len(bodyArray)
    
    for i in range(endIndex):
        #Input Desc
        if bodyArray[i] == "Input":
            inputIndex = i
        elif bodyArray[i] == "Input Format:":
            inputIndex = i
        elif bodyArray[i] == "Input Specification":
            inputIndex = i
        #Output Desc
        if bodyArray[i] == "Output":
            outputIndex = i
        elif bodyArray[i] == "Output Format:":
            outputIndex = i
        elif bodyArray[i] == "Output Specification":
            outputIndex = i
        #Examples Desc
        if sampleIndex != -1:
            sampleIndex = sampleIndex
        elif bodyArray[i] == "Samples":
            sampleIndex = i
        elif "Sample Input" in bodyArray[i]:
            sampleIndex = i
        elif "Example" in bodyArray[i]:
            sampleIndex = i
        #Notes
        if bodyArray[i] == "Notes:":
            notesIndex = i
        elif bodyArray[i] == "Note:":
            notesIndex = i
        elif "Note" in bodyArray[i]:
            note = bodyArray[i].split("Note")
            if len(note[0]) < 1:
                notesIndex = i
        #followup
        if bodyArray[i] == "Follow up:":
            followupIndex = i
        #Constraints
        if bodyArray[i] == "Constraints":
            constraintsIndex = i
        elif "Constraints" in bodyArray[i]:
            constraintsIndex = i
        #Time Limit
        if "time limit" in bodyArray[i].lower():
            timeLimitIndex = i
        #memory Limit
        if "memory limit" in bodyArray[i].lower():
            memoryLimitIndex = i
    
    indexes = [startIndex, inputIndex, outputIndex, sampleIndex, notesIndex, followupIndex, constraintsIndex, endIndex, timeLimitIndex, memoryLimitIndex]
    indexes.sort()
    data = {}
    
    title = page.title
    problemName = title.text
    
    data["Title"] = problemName
    
    for i in range(len(indexes)):
        if indexes[i] == -1:
            continue
        if (i+1) == (len(indexes)):
            continue
        
        if indexes[i] == 0:
            data["Description"] = util.getTextInfo(bodyArray, indexes[i], indexes[i+1])
        elif "Sample Input" in bodyArray[indexes[i]]:
            data["Example"] = util.getTextInfo(bodyArray, indexes[i], indexes[i+1])
        elif "Example" in bodyArray[indexes[i]]:
            data["Example"] = util.getTextInfo(bodyArray, indexes[i], indexes[i+1])
        elif "Time" in bodyArray[indexes[i]]:
            data["Time Limit"] = util.getTextInfo(bodyArray, indexes[i], indexes[i+1])
        elif "Memory" in bodyArray[indexes[i]]:
            data["Memory Limit"] = util.getTextInfo(bodyArray, indexes[i], indexes[i+1])
        else:
            title = bodyArray[indexes[i]].replace(":", "")
            data[title] = util.getTextInfo(bodyArray, indexes[i], indexes[i+1])
    
    util.writeToJSON(crawlerType, extractorType, domain, fileName, data)