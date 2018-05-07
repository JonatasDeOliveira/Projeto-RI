from bs4 import BeautifulSoup
from selenium import webdriver
import reader as r


soup = r.get_link("https://www.urionlinejudge.com.br/judge/en/problems/view/1001")

print (soup)
