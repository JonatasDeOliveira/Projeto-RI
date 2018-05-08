from bs4 import BeautifulSoup
from selenium import webdriver
import signal
import util

def leetcode(page, crawlerType, extractorType, domain, fileName):
    #driver = webdriver.PhantomJS()
    #driver.get("https://leetcode.com/problems/minimum-time-difference/description/")
    #page = BeautifulSoup(driver.page_source, "html.parser")
    #driver.service.process.send_signal(signal.SIGTERM)
    
    data = {}
    
    problemHead = page.find("div", {"class" : "col-lg-8 col-md-7 col-sm-6 col-sm-pull-6 col-md-pull-5 col-lg-pull-4"})
    problemBody = page.find("div", {"class" : "question-description"})
    
    problemName = problemHead.h3.text
    
    bodyText = problemBody.text
    bodyArray = bodyText.split("\n")
    bodyText = problemBody.find_all(["p", "pre", "li"])
    
    data["Title"] = problemName
    elementTitle = "Description"
    elementContent = ""
    
    for element in bodyArray:
        if "Note:" in element:
            data[elementTitle] = elementContent[:-1]
            elementTitle = "Note"
            if len(element.replace("Note:", "")) > 1:
                elementContent = element.replace("Note: ", "")
            else:
                elementContent = ""
        elif "Example" in element:
            if elementTitle == "Example":
                continue
            else: 
                data[elementTitle] = elementContent[:-1]
                elementTitle = "Example"
                elementContent = ""
        elif "Follow up:" in element:
            data[elementTitle] = elementContent[:-1]
            elementTitle = "Follow up"
            elementContent = ""
        else:
            elementContent += element + "\n"
    data[elementTitle] = elementContent
    
    util.writeToJSON(crawlerType, extractorType, domain, fileName, data)