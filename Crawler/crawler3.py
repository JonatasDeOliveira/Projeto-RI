from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from selenium import webdriver
from reppy.robots import Robots
from reppy.cache import RobotsCache
from Classifier.classifier import Classifier
import re
import requests
import queue
import time
import os
import signal
from Extractor import extractorMain

r = "http://www.codeforces.com"
i = 0
def robots(pathTotal, rp):
    return rp.allowed(pathTotal,"*")

def get_all_links(domain, pathTotal, maxSize, rp, driver):
    #response = requests.get(domain+path, headers={'User-Agent': 'Mozilla/5.0'})
    driver.get(pathTotal)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    links = []
    for link in soup.findAll('a', href=True):
        regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if(((re.match(regex, domain+link.get('href')) is not None or re.match(regex, domain+'/'+link.get('href')) is not None) and (re.match(regex, link.get('href')) is None) and (link.get('href')!='javascript:void();')) or (domain in link.get('href'))):
            if(len(link.get('href'))>0):
                if(domain in link.get('href')):
                    if(robots(link.get('href'), rp)):
                        #print(link.get('href'))
                        try:
                            r = requests.get(link.get('href'), verify=False)
                            if "text/html" in r.headers["content-type"]:    
                                links.append(link.get('href'))
                        except:
                            pass
                elif((link.get('href')[0]>='a'and link.get('href')[0]<='z') or (link.get('href')[0]>='1'and link.get('href')[0]<='9')):
                    if(robots(domain+'/'+link.get('href'), rp)):
                        #print(domain+'/'+link.get('href'))
                        try:
                            r = requests.get(domain+'/'+link.get('href'), verify=False)
                            if "text/html" in r.headers["content-type"]:    
                                links.append(domain+'/'+link.get('href'))
                        except:
                            pass
                else:
                    if(robots(domain+link.get('href'), rp)):
                        #print(domain+link.get('href'))
                        try:
                            r = requests.get(domain+link.get('href'), verify=False)
                            if "text/html" in r.headers["content-type"]:  
                                links.append(domain+link.get('href'))
                        except:
                            pass
        
    return links


def crawler(domain, pathseed, uniqueId, maxSize = 5000):
    pq = queue.PriorityQueue()
    visited = []
    links = []
    pq.put((value(domain+pathseed),domain+pathseed))
    visited.append(domain+pathseed)
    rp = Robots.fetch(domain+'/robots.txt',verify=False)
    driver = webdriver.PhantomJS( service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
    while(not pq.empty() and pq.qsize()<maxSize*5):
        a = pq.get()[1]
        print("! " + str(len(links)) + " " + a)
        if(len(links) < maxSize):
            links.append(a)
            ls = get_all_links(domain, a, maxSize, rp, driver)
            for l in ls:
                if(l not in visited):
                    if(value(l)==1 or value(l)==2):
                        visited.append(l)
                        pq.put((value(l),l))
        else:
            while(not pq.empty()):
                pq.get()
    while(len(links)<maxSize and not pq.empty()):
        links.append(pq.get()[1])
    os.makedirs('Docs/HTMLPages/Heuristic2/'+folder(domain)+'/True/', exist_ok=True)
    os.makedirs('Docs/HTMLPages/Heuristic2/'+folder(domain)+'/False/', exist_ok=True)
    print(len(links))
    v = 0
    clf = Classifier()
    pos = 0
    res = ""
    for l in links:
        v += 1
        driver.get(l)
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        res =  str(clf.classify(soup))
        print(str(v)+ " "+l + " "+ res)
        #print(driver.page_source)
        if(res == 'True'):
            pos += 1
            extractorMain.extractor(soup, folder(domain), "Heuristic2", folder(domain).lower(), l, uniqueId)
            uniqueId += 1
        with open('Docs/HTMLPages/Heuristic2/'+folder(domain)+'/'+res+'/'+str(v) +'-'+l.replace('/','*')+'.html', 'wb') as f:
            f.write(bytes(driver.page_source,'UTF-8'))
    hr = pos/maxSize
    with open('Docs/HTMLPages/Heuristic2/'+folder(domain)+'/'+'hr.txt', 'wb') as f:
        f.write(bytes(str(hr),'UTF-8'))
    return 0


def folder(domain):
    if(domain=="http://www.codeforces.com"):
        return 'Codeforces'
    if(domain=='https://www.spoj.com'):
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
    if(domain=='https://www.codechef.com'):
        return 'Codechef'
    if(domain=='https://a2oj.com'):
        return 'A2oj'

def value(link):
    if("http://www.codeforces.com" in link):
        if('problem/' in link and 'problemset' in link):
            return 1
        elif('problemset' in link and ('tag' in link or 'page' in link)):
            return 2
        elif('problemset' in link):
            return 2
        else:
            return 3
    if('https://www.spoj.com' in link):
        if('problems' in link and ('tag' in link or 'classical' in link) and 'cstart' not in link and 'lang' not in link and 'main' not in link ):
            return 2
        elif('problems/' in link and 'cstart' not in link and 'lang' not in link and 'main' not in link):
            return 1
        elif('problems' in link and 'cstart' not in link and 'lang' not in link and 'main' not in link):
            return 2
        else:
            return 3
    if('https://dmoj.ca' in link):
        if('rank' in link or 'submissions' in link or 'submit' in link or 'comment' in link or 'login' in link or 'register' in link or 'user' in link or 'contest' in link):
            return 4
        elif('problems' in link):
            return 2
        elif('problem' in link):
            return 1
        else:
            return 3
    if('https://wcipeg.com' in link):
        if('login' in link or 'announcement' in link or 'comment' in link or 'auth' in link or 'main' in link or 'organizations' in link or 'user' in link or 'submissions' in link or 'submit' in link or 'comment' in link or 'search' in link):
            return 4
        elif('problems' in link):
            return 2
        elif('problem' in link):
            return 1
        else:
            return 3
    if('http://acm.timus.ru' in link):
        if('locale' in link or 'sort' in link):
            return 4
        elif('problemset' in link):
            return 2
        elif('problem' in link):
            return 1
        else:
            return 3
    if('https://www.urionlinejudge.com.br' in link):
        if('categories' in link):
            return 3
        elif('problems' in link and 'view' in link):
            return 1
        elif('problems' in link):
            return 2
        else:
            return 4
    if('https://leetcode.com' in link):
        if('problemset' in link):
            return 2
        elif('problems' in link and 'description' not in link and 'hints' not in link and 'submissions' not in link and 'discuss' not in link and 'solution' not in link):
            return 1
        else:
            return 3
    if('https://www.codechef.com' in link):
        if('problems' in link and ('school' in link or 'easy' in link or 'medium' in link or 'hard' in link or 'challenge' in link or 'extcontest' in link)):
            return 2
        elif('problems' in link):
            return 1
        else:
            return 3
    if('https://a2oj.com' in link):
        if('/ps' in link):
            return 2
        elif('/p' in link and '?ID' in link):
            return 1
        else:
            return 3
    return 5

#crawler('https://wcipeg.com','', 0)
crawler('http://www.codeforces.com','', 5000)
#crawler('https://a2oj.com','', 2000)
##crawler('https://www.codechef.com','')
#crawler('http://acm.timus.ru','', 3000)
#crawler('https://www.spoj.com','', 4000)
#crawler('https://dmoj.ca','', 5000) 
##crawler('https://www.urionlinejudge.com.br','')
##crawler('https://leetcode.com','')H