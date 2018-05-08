import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup
import signal
from classifier import Classifier

url = "http://www.spoj.com/problems/MMIND/"
driver = webdriver.PhantomJS( service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
driver.get(url)
page = BeautifulSoup(driver.page_source, "html.parser")
driver.service.process.send_signal(signal.SIGTERM)

clf = Classifier()
print(clf.classify(page))