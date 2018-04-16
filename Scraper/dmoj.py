import bs4 as bs
import requests
import util

request = requests.get("https://dmoj.ca/problem/apio10p2")

page = bs.BeautifulSoup(request.content, "html.parser")

datas = []

problemHead = page.find("div", {"class": "problem-title"})
problemName = problemHead.h2.text

datas.append(problemName)

problem = page.find("div", {"class": "content-description screen"})
problemBody = problem.div

problemInfos = problemBody.findAll(["h4", "p", "pre"])

datas = util.getDatas(datas, problemInfos, "h4")

limits = page.findAll("div", {"class": "problem-info-entry"})

problemTime = limits[1].text[1:-1]
problemMemory = limits[2].text[1:-1]
datas.append(problemTime)
datas.append(problemMemory)

for i in datas:
    print (i) 
    print ("\n")