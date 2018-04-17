from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib import robotparser
import re
import requests
import queue


r = "http://www.codeforces.com"
i = 0

def robots(domain, path, rp):
    return rp.can_fetch("*", domain+path)

def get_all_links(domain, path):
    req = Request(domain+path)
    html_page = urlopen(req)
    soup = BeautifulSoup(html_page, "html5lib")
    links = []
    rp = robotparser.RobotFileParser()
    rp.set_url(domain+"/robots.txt")
    rp.read()
    for link in soup.findAll('a'):
        if(robots(domain, link.get('href'), rp)):
            links.append(link.get('href'))
    return links


def crawler(domain, pathseed, maxSize = 10):
    q = queue.Queue()
    visited = []
    links = []
    q.put(pathseed)
    visited.append(pathseed)
    while(not q.empty()):
        a = q.get()
        if(len(links) < maxSize):
            links.append(domain+a)
            ls = get_all_links(domain, a)
            for l in ls:
                if(l not in visited):
                    visited.append(l)
                    q.put(l)
        else:
            while(not q.empty()):
                q.get()
                
    for l in links:
        print(l)
        response = urlopen(l)
        webContent = response.read()
        f = open('Docs/HTMLPages/'+folder(domain)+'/'+l.replace('/','*')+'.html', 'wb')
        f.write(webContent)
        f.close
    return 0

def folder(domain):
    if(domain=="http://www.codeforces.com"):
        return 'Codeforces'
    
    
crawler("http://www.codeforces.com",'/problemset/')