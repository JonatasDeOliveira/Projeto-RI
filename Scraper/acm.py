import requests
import bs4 as bs
import util
import re
import math

request = requests.get("http://acm.timus.ru/problem.aspx?space=1&num=1065")
page = bs.BeautifulSoup(request.content, "html.parser")

problem = page.find("div", {"class": "problem_content"})
problemName = problem.h2.text

problemLimits = problem.find("div", {"class" : "problem_limits"})
limit = util.treatStr(problemLimits)

limits = limit.split("\n")

problemTime = limits[0]
problemMemory = limits[1]

problemBody = page.find("div", {"id": "problem_text"})
problemText = problemBody.findAll(["div", "h3"])
texts = []

count = 0
for text in problemText:
    info = text.text
    if info not in texts:
        if "Problem Author:" in info:
            texts.append("Problem Author:")
        else:
            texts.append(info)

inputIndex = util.findTextIndex(texts, "Input")
outputIndex = util.findTextIndex(texts, "Output")
exampleIndex = util.findTextIndex(texts, "Sample")
if exampleIndex is None:
    exampleIndex = util.findTextIndex(texts, "Samples")
    
notesIndex = util.findTextIndex(texts, "Notes")
authorIndex = util.findTextIndex(texts, "Problem Author:")

problemDescripton = ""
problemInputDes = ""
problemOutputDes = ""
problemNotes = ""

if inputIndex is None:
    problemDescripton = util.getTextInfo(texts, 0, exampleIndex)
else:
    problemDescripton = util.getTextInfo(texts, 0, inputIndex)
    problemInputDes = util.getTextInfo(texts, inputIndex, outputIndex)
    problemOutputDes = util.getTextInfo(texts, outputIndex, exampleIndex)
    
if notesIndex is not None:
    problemNotes = util.getTextInfo(texts, exampleIndex + 1, authorIndex)

print (problemDescripton)
print (problemInputDes)
print (problemOutputDes)
print (problemNotes)

samples = problemBody.find("table", {"class" : "sample"})

tableTitles = samples.findAll("th")
tableInfos = samples.findAll("pre")

problemSamples = tableTitles[0].text + "\n" + util.getEvenText(tableInfos) + tableTitles[1].text + "\n" + util.getOddText(tableInfos)

print (problemSamples)
#http://acm.timus.ru/problem.aspx?space=1&num=1082