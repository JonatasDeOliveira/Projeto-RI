from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from selenium import webdriver
from reppy.cache import RobotsCache
import re
import requests
import queue
import time
import os

r = "http://www.codeforces.com"
i = 0

def rrobots(domain, path, rp):
    return rp.allowed(domain+path,"*")

def get_all_links(domain, path, maxSize):
    #response = requests.get(domain+path, headers={'User-Agent': 'Mozilla/5.0'})
    driver = webdriver.PhantomJS()
    driver.get(domain+path)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    links = []
    rp = RobotsCache(10000)
    for div in soup.findAll('div'):
        for link in div.findAll('a', href=True):
            #print(link.get('href'))
            if(rrobots(domain, link.get('href'), rp)):
                regex = re.compile(
                    r'^(?:http|ftp)s?://' # http:// or https://
                    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                    r'localhost|' #localhost...
                    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                    r'(?::\d+)?' # optional port
                    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
                if re.match(regex, domain+link.get('href')) is not None:
                    if(len(link.get('href'))>0):
                        if((link.get('href')[0]>='a'and link.get('href')[0]<='z') or (link.get('href')[0]>='1'and link.get('href')[0]<='9')):
                            links.append('/'+link.get('href'))
                        else:
                            links.append(link.get('href'))
    return links


def crawler(domain, pathseed, maxSize = 100):
    q = queue.Queue()
    visited = []
    links = []
    q.put(pathseed)
    visited.append(pathseed)
    while(not q.empty() and q.qsize()<maxSize):
        a = q.get()
        print("! " + str(q.qsize()))
        if(len(links) < maxSize):
            links.append(domain+a)
            ls = get_all_links(domain, a, maxSize)
            for l in ls:
                if(l not in visited):
                    visited.append(l)
                    q.put(l)
        else:
            while(not q.empty()):
                q.get()
    while(len(links)<maxSize and not q.empty()):
        links.append(domain+q.get())
    os.makedirs('Docs/HTMLPages/'+folder(domain)+'/', exist_ok=True)
    print(len(links))
    for l in links:
        print(l)
        driver = webdriver.PhantomJS()
        driver.get(l)
        #print(driver.page_source)
        with open('Docs/HTMLPages/'+folder(domain)+'/'+l.replace('/','*')+'.html', 'wb') as f:
            f.write(bytes(driver.page_source,'UTF-8'))
        driver.service.process.send_signal(signal.SIGTERM) 
        driver.quit() 
    return 0


def folder(domain):
    if(domain=="http://www.codeforces.com"):
        return 'Codeforces'
    if(domain=='http://www.spoj.com'):
        return 'Spoj'
    if(domain=='https://dmoj.ca'):
        return 'Dmoj'
    if(domain=='https://wcipeg.com'):
        return 'Wcipeg'
    if(domain=='http://acm.timus.ru'):
        return 'Timus'
    if(domain=='https://www.urionlinejudge.com.br'):
        return 'Uri'
    if(domain=='https://leetcode.com'):
        return 'Leetcode'
    
crawler('https://leetcode.com','')
#crawler('https://dmoj.ca','')

