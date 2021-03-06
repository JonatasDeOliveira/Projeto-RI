import requests
import bs4 as bs
from Extractor import util

def spoj(page, link, uniqueId):
    #request = requests.get("http://www.spoj.com/problems/TTABLE/")
    #page = bs.BeautifulSoup(request.content, "html.parser")
        
    dataT = {}
        
    #Container da descricao do problema
    problem = page.find("div", {"class" : "prob"})
    
    name = problem.find("h2", {"id" : "problem-name"})
    problemName = name.text
    dataT["Title"] = problemName
        
    tags = page.find("div", {"id" : "problem-tags"})
    problemTags = ""
    if len(tags) >= 1:
        problemTags = (tags.text)[1:]
        problemTags = problemTags.replace("#", " - ")
        
    problemBody = problem.find("div", {"id" : "problem-body"})
    
    #contents
    problemArray = problemBody.text
    problemArray = problemArray.split("\n")
    
    elementTitle = "Description"
    elementContent = ""
    for element in problemArray:
        if (element == "Input") or (element == "Output") or (element == "Example"):
            dataT[elementTitle] = elementContent[:-1]
            elementTitle = element
            elementContent = ""
        else:
            elementContent += element + "\n"
    dataT[elementTitle] = elementContent[:-1]
    
    #time and memory limit
    problemInfo = page.find("div", {"class" : "col-lg-4 col-md-4"})
    table = problemInfo.find("table", {"id" : "problem-meta"})
    rows = table.findAll("tr")
    
    for row in rows:
        if "Time" in row.text:
            info = (row.text).split("limit:")
            dataT["Time Limit"] = info[1]
        else:
            if "Memory" in row.text:
                info = (row.text).split("limit:")
                dataT["Memory Limit"] = info[1]
    
    dataT["Problem"] = util.getText(problem) + "\n" + util.getText(table)
    dataT["URL"] = link
    
    data = {}
    data[uniqueId] = dataT
    
    util.loadData(data)