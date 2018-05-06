from bs4 import BeautifulSoup
import requests
import re
import util

request = requests.get("https://a2oj.com/p?ID=134", verify = False)
page = BeautifulSoup(request.content, "html.parser")

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

data = {"Title" : problemName,
        "Description" : problemDescripton,
        "Input Description" : problemInput,
        "Output Description" : problemOutput,
        "Example" : problemSamples,
        "Notes" : problemNotes,
        "Time Limit" : problemTimeLimit}

print (data)
for d in data:
    print (d + ": \n" + data[d])
    print ("----------------")