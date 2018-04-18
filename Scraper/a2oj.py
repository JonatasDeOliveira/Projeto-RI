import bs4 as bs
import requests
import re
import util

request = requests.get("https://a2oj.com/p?ID=134", verify = False)
page = bs.BeautifulSoup(request.content, "html.parser")

datas = []

problem = page.find("div", {"id":"page"})
reName = re.findall('[0-9].*?\n', problem.div.text)
problemName = reName[0]
problemName = problemName[:-1]

problemBody = problem.findAll("div")

problemIndex = util.findIndex(problemBody, "Problem Statement:")
inputIndex = util.findIndex(problemBody, "Input Format:")
outputIndex = util.findIndex(problemBody, "Output Format:")
sampleInIndex = util.findIndex(problemBody, "Sample Input:")
sampleOutIndex = util.findIndex(problemBody, "Sample Output:")
notesIndex = util.findIndex(problemBody, "Notes:")

problemDescripton = util.getInfo(problemBody, problemIndex, problemIndex + 2)
problemInput = util.getInfo(problemBody, inputIndex, inputIndex + 2)
problemOutput = util.getInfo(problemBody, outputIndex, outputIndex + 2)
problemSampleIn = util.getInfo(problemBody, sampleInIndex, sampleInIndex + 2)
problemSampleOut = util.getInfo(problemBody, sampleOutIndex, sampleOutIndex + 2)
problemSamples = problemSampleIn + problemSampleOut

problemNotes = ""
if notesIndex is not None:
    problemNotes = util.getInfo(problemBody, notesIndex, notesIndex + 2)

datas.append(problemName)
datas.append(problemDescripton)
datas.append(problemInput)
datas.append(problemOutput)
datas.append(problemSamples)
datas.append(problemNotes)

table = problemBody[-1].findAll("tr")
for t in table:
    if "Time Limit:" in t.text:
        datas.append(t.text)
        break

for i in datas:
    print (i) 