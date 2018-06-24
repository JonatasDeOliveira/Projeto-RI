import requests
from bs4 import BeautifulSoup
import re
import util
import json
from selenium import webdriver
import signal
import os
import wcipeg

"""
driver = webdriver.PhantomJS()
driver.get("https://wcipeg.com/problem/a1")
page = BeautifulSoup(driver.page_source, "html.parser")
driver.service.process.send_signal(signal.SIGTERM)


for d in data:
    print (d + ":\n" + data[d])
    print ( "--------------------")
    
    #https://stackoverflow.com/questions/30539679/python-read-several-json-files-from-a-folder
    
"""

name = "./Docs/HTMLPages/Heuristic2/Wcipeg/True/"

file_list = os.listdir(name)
uniqueId = 0
for file in file_list:
    
    result = re.findall('[0-9]*?\-', file)
    link = file.replace(result[0], "")
    link = link.replace('*', '/')
    
    place = name + file

    entrada = open(place, "rb")
    page = entrada.read()
    wcipeg.wcipeg(page, "", "", "", "", link, uniqueId)
    uniqueId = uniqueId + 1
    