import requests
import bs4 as bs
import util

def getSpojData(url):
    request = requests.get(url)
    page = bs.BeautifulSoup(request.content, "html.parser")
    
    data = {}
    
#Container da descricao do problema
    problem = page.find("div", {"class" : "prob"})
    name = problem.find("h2", {"id" : "problem-name"})
    problemName = name.text
    
    tags = page.find("div", {"id" : "problem-tags"})
    
    problemTags = (tags.text)[1:]
    problemTags = problemTags.replace("#", " - ")
    
    problemBody = problem.find("div", {"id" : "problem-body"})
    
    #Pega as descricoes do problema
    elements = problemBody.findAll(["p", "h3", "pre"])

    inputIndex = util.findIndex(elements, "Input")
    outputIndex = util.findIndex(elements, "Output")
    exampleIndex = util.findIndex(elements, "Example")
    infoIndex = util.findIndex(elements, "Information")
    
    problemInputDes = ""
    problemOutputDes = ""
    
    if inputIndex is None:
        problemDescripton = util.getInfo(elements, 0, exampleIndex-1)
    else:
        problemDescripton = util.getInfo(elements, 0, inputIndex)
        problemInputDes = util.getInfo(elements, inputIndex + 1, outputIndex)
        problemOutputDes = util.getInfo(elements, outputIndex + 1, exampleIndex)
    
    if infoIndex is None:
        problemExample = util.getInfo(elements, exampleIndex + 1, len(elements))
    else:
        problemExample = util.getInfo(elements, exampleIndex + 1, infoIndex)
    
    data = {"Title" : problemName,
        "Tags" : problemTags,
        "Description" : problemDescripton,
        "Input Description" : problemInputDes,
        "Output Description" : problemOutputDes,
        "Example" : problemExample}
    #Container informacoes do problema
    problemInfo = page.find("div", {"class" : "col-lg-4 col-md-4"})
    
    table = problemInfo.find("table", {"id" : "problem-meta"})
    
    rows = table.findAll("tr")
    for row in rows:
        if "Time" in row.text:
            info = (row.text).split("limit:")
            data["Time Limit"] = info[1]
        else:
            if "Memory" in row.text:
                info = (row.text).split("limit:")
                data["Memory Limit"] = info[1]
    print(data)
    return (data)
   
    
sites = {"http://www.spoj.com/problems/TEST/", "http://www.spoj.com/problems/SBSTR1/", "http://www.spoj.com/problems/ARITH/", "http://www.spoj.com/problems/ONP/"}

for site in sites:
    getSpojData(site)
    print ("\n")