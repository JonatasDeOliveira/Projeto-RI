import bs4 as bs
import requests
import util

request = requests.get("https://dmoj.ca/problem/asm1")

page = bs.BeautifulSoup(request.content, "html.parser")

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

print (bodyArray)
for i in range(endIndex):
    #Input Desc
    if bodyArray[i] == "Input Specification":
        inputIndex = i
    #Output Desc
    if bodyArray[i] == "Output Specification":
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
    if bodyArray[i] == "Constraints":
        constraintsIndex = i
    #Time Limit
    if "time limit" in bodyArray[i].lower():
        timeLimitIndex = i

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
        data[bodyArray[indexes[i]]] = util.getTextInfo(bodyArray, indexes[i], indexes[i+1])


#problemInfos = problemBody.findAll(["h4", "p", "pre"])
#datas = util.getDatas(datas, problemInfos, "h4")
limits = page.findAll("div", {"class": "problem-info-entry"})

problemTime = limits[1].text[1:-1]
problemMemory = limits[2].text[1:-1]

data["Ttile"] = problemName
data["Time Limit"] = problemTime
data["Memory Limit"] = problemMemory

for d in data:
    print (data[d] + "\n\n")