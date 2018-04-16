import requests
import bs4
import re

def treatStr(sample):
    samples = re.findall('\>.*?\<',str(sample))
    sampleStr = ""
    for s in samples:
        if len(s) > 2:
            newS = s.replace(">", "")
            newS = newS.replace("<", "")
            sampleStr += newS + "\n"
    return sampleStr[:-1]
    
request = requests.get("http://codeforces.com/problemset/problem/949/A")
page = BeautifulSoup.BeautifulSoup(request.content)
    
data = []
    
#Container da descricao do problema
problem = page.find("div", {"class" : "problem-statement"})

name = problem.find("div", {"class" : "title"})
problemName = name.text

time = problem.find("div", {"class" : "time-limit"})
timeText = time.text
problemTime = timeText.replace("time limit per test", "")

memory = problem.find("div", {"class" : "memory-limit"})
memoryText = memory.text
problemMemory = memoryText.replace("memory limit per test", "")

description = problem.findAll("div")[10]
problemDescripton = description.text

inputDescripton = problem.find("div", {"class" : "input-specification"})
problemInput = inputDescripton.text[5:]

outputDescripton = problem.find("div", {"class" : "output-specification"})
problemOutput = outputDescripton.text[6:]

sampleTest = problem.find("div", {"class" : "sample-test"})
samplesInput = sampleTest.findAll("div", {"class" : "input"})
samplesOutput = sampleTest.findAll("div", {"class" : "output"})
problemSample = ""

for i in range(len(samplesInput)):
    problemSample += treatStr(samplesInput[i]) + "\n" + treatStr(samplesOutput[i]) + "\n\n"
    
print problemSample[:-2]