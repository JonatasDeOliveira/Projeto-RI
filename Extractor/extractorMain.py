from Extractor import a2oj
from Extractor import codeforces
from Extractor import dmoj
from Extractor import leetcode
from Extractor import spoj
from Extractor import timus
from Extractor import wcipeg
from Extractor import genericExtractor as g1
from Extractor import genericExtractor2 as g2
import os

def extractor(page, domain, crawlerType, fileName, link, uniqueId):
    
    os.makedirs('Docs/Jsons/', exist_ok=True)
    os.makedirs('Docs/Jsons/' + crawlerType + '/Specific/' + domain, exist_ok=True)
    os.makedirs('Docs/Jsons/' + crawlerType + '/General_1/' + domain, exist_ok=True)
    os.makedirs('Docs/Jsons/' + crawlerType + '/General_2/' + domain, exist_ok=True)
    
    
    if domain == "A2oj":
        a2oj.a2oj(page, crawlerType, "Specific", domain, fileName, link, uniqueId)
    elif domain == "Codeforces":
        codeforces.codeforces(page, crawlerType, "Specific", domain, fileName, link, uniqueId)
    elif domain == "Dmoj":
        dmoj.dmoj(page, crawlerType, "Specific", domain, fileName, link, uniqueId)
    elif domain == "Leetcode":
        leetcode.leetcode(page, crawlerType, "Specific", domain, fileName, link, uniqueId)
    elif domain == "Spoj":
        spoj.spoj(page, crawlerType, "Specific", domain, fileName, link, uniqueId)
    elif domain == "Timus":
        timus.timus(page, crawlerType, "Specific", domain, fileName, link, uniqueId)
    elif domain == "Wcipeg":
        wcipeg.wcipeg(page, crawlerType, "Specific",domain,  fileName, link, uniqueId)
    
#    g1.genericExtractor(page, crawlerType, "General_1", domain, fileName)
#    g2.genericExtractor2(page, crawlerType, "General_2", domain, fileName)