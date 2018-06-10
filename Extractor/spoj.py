import requests
import bs4 as bs
from Extractor import util

def spoj(page, crawlerType, extractorType, domain, fileName):
    #request = requests.get("http://www.spoj.com/problems/TTABLE/")
    #page = bs.BeautifulSoup(request.content, "html.parser")
        
    data = {}
        
    #Container da descricao do problema
    problem = page.find("div", {"class" : "prob"})
    
    name = problem.find("h2", {"id" : "problem-name"})
    problemName = name.text
    data["Title"] = problemName
        
    tags = page.find("div", {"id" : "problem-tags"})
        
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
            data[elementTitle] = elementContent[:-1]
            elementTitle = element
            elementContent = ""
        else:
            elementContent += element + "\n"
    data[elementTitle] = elementContent[:-1]
    
    #time and memory limit
    problemInfo = page.find("div", {"class" : "col-lg-4 col-md-4"})
    table = problemInfo.find("table", {"id" : "problem-meta"})
        
    rows = table.findAll("tr")
    for row in rows:
        if "Time" in row.text:
            info = (row.text).split("limit:")
            data["Time Limit"] = info[1]
        else:
            if "Memory" in row.text:
                info = (row.text).split("limit:")
                data["Memory Limit"] = info[1]
            
    util.writeToJSON(crawlerType, extractorType, domain, fileName, data)