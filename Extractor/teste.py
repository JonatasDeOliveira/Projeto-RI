import requests
import bs4 as bs
import re
import util

request = requests.get("http://acm.timus.ru/problem.aspx?space=1&num=1218")
page = bs.BeautifulSoup(request.content, "html.parser")
    
problem = page.find("div", {"class": "problem_content"})
    
title = page.title
title = title.text
problemName = title.replace(" @ Timus Online Judge", "")

problemLimits = problem.find("div", {"class" : "problem_limits"})
limit = util.treatStr(problemLimits)
limits = limit.split("\n")

problemTime = limits[0].replace("Time limit: ", "")
problemMemory = limits[1].replace("Memory limit: ", "")

problemBody = page.find("div", {"id": "problem_text"})
problemText = problemBody.findAll(["div", "h3"])
texts = []

count = 0
for text in problemText[:-1]:
    info = text.text
    texts.append(info)

inputIndex = util.findTextIndex(texts, "Input")
outputIndex = util.findTextIndex(texts, "Output")
exampleIndex = util.findTextIndex(texts, "Sample")
lastIndex = len(texts)

if exampleIndex is None:
    exampleIndex = util.findTextIndex(texts, "Samples")
    
notesIndex = util.findTextIndex(texts, "Notes")

problemDescripton = ""
problemInputDes = ""
problemOutputDes = ""
problemNotes = ""

if inputIndex is None:
    problemDescripton = util.getTextInfo(texts, 0, exampleIndex)
else:
    problemDescripton = util.getTextInfo(texts, 0, inputIndex)
    problemInputDes = util.getTextInfo(texts, inputIndex + 1, outputIndex)
    
    if exampleIndex is not None:
        problemOutputDes = util.getTextInfo(texts, outputIndex + 1, exampleIndex)
    elif notesIndex is not None:
        problemOutputDes = util.getTextInfo(texts, outputIndex + 1, notesIndex)
    else:
        problemOutputDes = util.getTextInfo(texts, outputIndex + 1, lastIndex)
        
if notesIndex is not None:
    problemNotes = util.getTextInfo(texts, exampleIndex + 1, lastIndex)

problemSamples = ""
samples = problemBody.find("table", {"class" : "sample"})
if samples is not None:
    tableTitles = samples.findAll("th")
    tableInfos = samples.findAll("pre")

    problemSamples = tableTitles[0].text + "\n" + util.getEvenText(tableInfos) + tableTitles[1].text + "\n" + util.getOddText(tableInfos)


data = {"Title" : problemName,
        "Description" : problemDescripton,
        "Input Description" : problemInputDes,
        "Output Description" : problemOutputDes,
        "Example" : problemSamples,
        "Notes" : problemNotes,
        "Time Limit" : problemTime,
        "Memory Limit" : problemMemory,
        "Problem" : util.getText(problem)
}
        
for d in data:
    print (d + " : " + data[d])
    print("-------------------------")