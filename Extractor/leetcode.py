from bs4 import BeautifulSoup
from selenium import webdriver
import signal
from Extractor import util

def leetcode(page, link, uniqueId):
    #driver = webdriver.PhantomJS()
    #driver.get("https://leetcode.com/problems/minimum-time-difference/description/")
    #page = BeautifulSoup(driver.page_source, "html.parser")
    #driver.service.process.send_signal(signal.SIGTERM)
    
    dataT = {}
    
    problemBody = page.find("div", {"class" : "question-description"})
    if problemBody is None:
        problemBody = page.find("div", {"class" : "question-description__3U1T"})
    
    title = page.title
    title = title.text
    problemName = title.replace(" - LeetCode", "")
    
    bodyText = problemBody.text
    bodyArray = bodyText.split("\n")
    bodyText = problemBody.find_all(["p", "pre", "li"])
    
    dataT["Title"] = problemName
    elementTitle = "Description"
    elementContent = ""
    
    for element in bodyArray:
        if "Note:" in element:
            dataT[elementTitle] = elementContent[:-1]
            elementTitle = "Note"
            if len(element.replace("Note:", "")) > 1:
                elementContent = element.replace("Note: ", "")
            else:
                elementContent = ""
        elif "Example" in element:
            if elementTitle == "Example":
                continue
            else: 
                dataT[elementTitle] = elementContent[:-1]
                elementTitle = "Example"
                elementContent = ""
        elif "Follow up:" in element:
            dataT[elementTitle] = elementContent[:-1]
            elementTitle = "Follow up"
            elementContent = ""
        else:
            elementContent += element + "\n"
    dataT[elementTitle] = elementContent
    
    title = page.find("div", {"class" : "question-title clearfix"})
    dataT["Problem"] = title.text + "\n" + problemBody.text
    dataT["URL"] = link
    
    data = {}
    data[uniqueId] = dataT
    
    util.loadData(data)