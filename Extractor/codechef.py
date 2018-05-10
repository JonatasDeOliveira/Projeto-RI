from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.PhantomJS()
driver.get("https://www.codechef.com/problems/H1")
page = BeautifulSoup(driver.page_source, "html.parser")
print (page.prettify())
