from bs4 import BeautifulSoup
import requests
import util
from selenium import webdriver
import signal
import time

request = requests.get("http://acm.timus.ru/problem.aspx?space=1&num=1000", verify = False)
page = BeautifulSoup(request.content, "html.parser")

mapList = {}

def walker(soup):
    if soup.name is not None:
        for child in soup.children:
            count = 0
            if "Input" in (str(child)):
                count += 1
            if "Output" in (str(child)):
                count += 1
            if "Example" in (str(child)):
                count += 1
            if "Sample" in (str(child)):
                count += 1
            if "Note" in (str(child)):
                count += 1
            if "Constraint" in (str(child)):
                count += 1
            if "Follow up" in (str(child)):
                count += 1
            if "time limit" in (str(child)).lower():
                count += 1
            if "memory limit" in (str(child)).lower():
                count += 1
            
            if util.checkMap(mapList, str(child.parent)):
                mapList[str(child.parent)] = count + mapList[str(child.parent)]
            else:
                mapList[str(child.parent)] = count
            walker(child)
            
def walker2(soup):
    if soup.name is not None:
        for child in soup.children:
            if child.name in ["p", "h2", "h3", "h4", "pre", "br"]:
                if util.checkMap(mapList, str(child.parent)):
                     mapList[str(child.parent)] = 1 + mapList[str(child.parent)]
                else:
                    mapList[str(child.parent)] = 1
            walker2(child)
            
walker(page)


body = BeautifulSoup(util.getMaxKey(mapList), "html.parser")
mapList = {}
print (body.text)
print("------------------------------------------------")
walker2(body)
body = BeautifulSoup(util.getMaxKey(mapList), "html.parser")
print (body.text)