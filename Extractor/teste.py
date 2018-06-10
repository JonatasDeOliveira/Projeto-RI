import bs4 as bs
import requests
import util

request = requests.get("https://a2oj.com/p?ID=134", verify = False)
page = bs.BeautifulSoup(request.content, "html.parser")

problem = page.find("div", {"id":"page"})
[s.extract() for s in page('script')]
print (problem.text)