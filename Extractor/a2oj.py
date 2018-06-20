from bs4 import BeautifulSoup
import requests
from Extractor import util

def a2oj(page, crawlerType, extractorType, domain, fileName, link, uniqueId):
    #request = requests.get("https://a2oj.com/p?ID=134", verify = False)
    #page = BeautifulSoup(request.content, "html.parser")
    
    problem = page.find("div", {"id":"page"})
    title = page.title
    title = title.text
    problemName = title.replace(" - A2 Online Judge", "")
    
    problemBody = problem.findAll("div")
    
    problemIndex = util.findIndex(problemBody, "Problem Statement:")
    inputIndex = util.findIndex(problemBody, "Input Format:")
    outputIndex = util.findIndex(problemBody, "Output Format:")
    sampleInIndex = util.findIndex(problemBody, "Sample Input:")
    sampleOutIndex = util.findIndex(problemBody, "Sample Output:")
    notesIndex = util.findIndex(problemBody, "Notes:")
    
    problemDescripton = util.getInfo(problemBody, problemIndex, inputIndex)
    problemInput = util.getInfo(problemBody, inputIndex, outputIndex)
    problemOutput = util.getInfo(problemBody, outputIndex, sampleInIndex)
    problemSampleIn = util.getInfo(problemBody, sampleInIndex, sampleOutIndex)
    problemSampleOut = util.getInfo(problemBody, sampleOutIndex, sampleOutIndex + 2)
    problemSamples = problemSampleIn + problemSampleOut
    
    problemNotes = ""
    if notesIndex is not None:
        problemNotes = util.getInfo(problemBody, notesIndex, notesIndex + 2)
    
    problemTimeLimit = ""
    table = problemBody[-1].findAll("tr")
    for t in table:
        if "Time Limit:" in t.text:
            problemTimeLimit = t.text
            problemTimeLimit = problemTimeLimit.replace("Time Limit:", "")
            problemTimeLimit = problemTimeLimit.replace("\n", "")
            break
    
    data = {"ID" : uniqueId,
            "URL" : link,
            "Title" : problemName,
            "Description" : problemDescripton,
            "Input Description" : problemInput,
            "Output Description" : problemOutput,
            "Example" : problemSamples,
            "Notes" : problemNotes,
            "Time Limit" : problemTimeLimit,
            "Problem" : util.getText(problem)
    }
        
    util.writeToJSON(crawlerType, extractorType, domain, fileName, data)