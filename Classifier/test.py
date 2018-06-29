import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup
import signal
from Classifier.classifier import Classifier

url = "http://www.spoj.com/problems/MMIND/"
driver = webdriver.PhantomJS( service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
driver.get(url)
page = BeautifulSoup(driver.page_source, "html.parser")
driver.service.process.send_signal(signal.SIGTERM)


k = [0,1,2,3,4,5]
for i in k:
    clf = Classifier(i)
    print(clf.classify(page))