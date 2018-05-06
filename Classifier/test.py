import urllib.request
from bs4 import BeautifulSoup
from classifier import Classifier

url = "http://www.spoj.com/status/"
html = urllib.request.urlopen(url)
page = BeautifulSoup(html, "html.parser")

clf = Classifier()
print(clf.classify(page))