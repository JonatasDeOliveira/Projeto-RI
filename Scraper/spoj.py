import requests
import bs4 

def findIndex(array, string):
    for i in range(0, len(array)):
        text = array[i].text
        if string == text:
            return i

def getInfo(array, s, e):
    info = ""
    for i in range(s, e):
        info += array[i].text + "\n"
    return info
    
def getSpojData(url):
    request = requests.get(url)
    page = BeautifulSoup.BeautifulSoup(request.content)
    
    data = []
    
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

    inputIndex = findIndex(elements, "Input")
    outputIndex = findIndex(elements, "Output")
    exampleIndex = findIndex(elements, "Example")
    infoIndex = findIndex(elements, "Information")
    
    problemInputDes = ""
    problemOutputDes = ""
    
    if inputIndex is None:
        problemDescripton = getInfo(elements, 0, exampleIndex)
    else:
        problemDescripton = getInfo(elements, 0, inputIndex)
        problemInputDes = getInfo(elements, inputIndex + 1, outputIndex)
        problemOutputDes = getInfo(elements, outputIndex + 1, exampleIndex)
    
    if infoIndex is None:
        problemExample = getInfo(elements, exampleIndex + 1, len(elements))
    else:
        problemExample = getInfo(elements, exampleIndex + 1, infoIndex)
    
    data.append(problemName)
    data.append(problemTags)
    data.append(problemDescripton)
    data.append(problemInputDes)
    data.append(problemOutputDes)
    data.append(problemExample)
    
    #Container informacoes do problema
    problemInfo = page.find("div", {"class" : "col-lg-4 col-md-4"})
    
    table = problemInfo.find("table", {"id" : "problem-meta"})
    
    rows = table.findAll("tr")
    for row in rows:
        if "Time" in row.text:
            info = (row.text).split("limit:")
            data.append(info[1])
        else:
            if "Memory" in row.text:
                info = (row.text).split("limit:")
                data.append(info[1])
    print(data)
    return data
   
    
sites = {"http://www.spoj.com/problems/TEST/", "http://www.spoj.com/problems/SBSTR1/", "http://www.spoj.com/problems/ARITH/", "http://www.spoj.com/problems/ONP/"}

for site in sites:
    getSpojData(site)
    print("\n")