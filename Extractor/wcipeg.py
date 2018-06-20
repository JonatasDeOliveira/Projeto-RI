import bs4 as bs
import requests
from Extractor import util

def wcipeg(page, crawlerType, extractorType, domain, fileName, link, uniqueId):
    #request = requests.get("https://wcipeg.com/problem/dt16l1p1")
    #page = bs.BeautifulSoup(request.content, "html.parser")
    
    problem = page.find("div", {"id": "descContent"})
    problemSidebar = page.find("div", {"id": "descSidebar"})
    
    data = {}
    
    title = page.title
    title = title.text
    problemName = title.replace("PEG Judge - ", "")
    
    #contents
    elements = problem.findAll(["h3", "p", "pre", "li"])
    
    if len(elements) == 0:
        elements = problem.findAll()
        elements = elements[1:]
    else:
        #Existem casos q o primeiro elemento é nome da universidade ou coisa do tipo.
        if elements[0].name == "h3":
            elements = elements[1:]
        
    elementTitle = "Description"
    elementContent = ""
    for element in elements:
        if element.name == "h3":
            if "Sample Input" in element.text:
                if elementTitle == "Example":
                    elementContent += element.text + "\n"
                else:
                    data[elementTitle] = elementContent[:-1]
                    elementTitle = "Example"
                    elementContent = "Sample Input \n"
            elif "Sample Output" in element.text:
                elementContent += element.text + "\n"
            else:
                data[elementTitle] = elementContent[:-1]
                elementTitle = element.text
                elementContent = ""
        else:
            elementContent += element.text + "\n"
            
    data[elementTitle] = elementContent[:-1]
            
    limits = problemSidebar.findAll("p")
    
    problemTime = util.findBetween(limits[3].text, "Time Limit: ", "\n")
    problemMemory = util.findBetween(limits[3].text, "Memory Limit: ", "\n")
    
    data["Title"] = problemName
    data["Time Limit"] = problemTime
    data["Memory Limit"] = problemMemory
    data["Problem"] = util.getText(problem) + "\n" + util.getText(problemSidebar)
    data["ID"] = uniqueId
    data["URL"] = link
    
    util.writeToJSON(crawlerType, extractorType, domain, fileName, data)