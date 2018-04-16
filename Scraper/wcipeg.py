import bs4 as bs
import requests
import util

request = requests.get("https://wcipeg.com/problem/acmtryouts3g")

page = bs.BeautifulSoup(request.content, "html.parser")
problem = page.find("div", {"id": "descContent"})
problemSidebar = page.find("div", {"id": "descSidebar"})

datas = []

problemName = problem.h2.text
datas.append(problemName)

problemInfos = problem.findAll(["h3", "p", "pre"])

text = ""

datas = util.getDatas(datas, problemInfos, "h3")
        
limits = problemSidebar.findAll("p")

problemTime = "Time Limit: " + util.findBetween(limits[3].text, "Time Limit: ", "\n")
problemMemory = "Memory Limi: " + util.findBetween(limits[3].text, "Memory Limit: ", "\n")

datas.append(problemTime)
datas.append(problemMemory)

for i in datas:
    print (i) 
    print ("\n")