from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib import robotparser
import re
import requests
import queue
import time


r = "http://www.codeforces.com"
i = 0

def robots(domain, path, rp):
	return rp.can_fetch("*", domain+path)

def get_all_links(domain, path, maxSize):
    response = requests.get(domain+path, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, "html.parser")
    links = []
    rp = robotparser.RobotFileParser()
    rp.set_url(domain+"/robots.txt")
    rp.read()
    for link in soup.findAll('a', href=True):
        if(robots(domain, link.get('href'), rp)):
            regex = re.compile(
                r'^(?:http|ftp)s?://' # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                r'localhost|' #localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                r'(?::\d+)?' # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            if re.match(regex, domain+link.get('href')) is not None:
                if((link.get('href')[0]>='a'and link.get('href')[0]<='z') or (link.get('href')[0]>='1'and link.get('href')[0]<='9')):
                    links.append('/'+link.get('href'))
                else:
                    links.append(link.get('href'))
    return links


def crawler(domain, pathseed, maxSize = 1000):
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
    for l in links:
        print(l)
        response = requests.get(l, headers={'User-Agent': 'Mozilla/5.0'})
        with open('Docs/HTMLPages/'+folder(domain)+'/'+l.replace('/','*')+'.html', 'wb') as f:
            f.write(response.content)
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
    
#crawler('https://wcipeg.com','')
crawler('https://dmoj.ca','')


#rp = robotparser.RobotFileParser()
#rp.set_url("https://dmoj.ca/robots.txt")
#rp.read()
#print(rp.can_fetch("*", 'https://dmoj.ca/problems/'))
