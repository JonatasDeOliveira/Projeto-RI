import bs4 as bs
import requests
import util

def wcipeg(page, crawlerType, extractorType, domain, fileName):
    #request = requests.get("https://wcipeg.com/problem/dt16l1p1")
    #page = bs.BeautifulSoup(request.content, "html.parser")
    
    problem = page.find("div", {"id": "descContent"})
    problemSidebar = page.find("div", {"id": "descSidebar"})
    
    data = {}
    
    problemName = problem.h2.text
    
    #contents
    elements = problem.findAll(["h3", "p", "pre", "li"])
    
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
    
    util.writeToJSON(crawlerType, extractorType, domain, fileName, data)