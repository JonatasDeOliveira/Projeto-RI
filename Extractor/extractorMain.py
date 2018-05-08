import a2oj
import codeforces
import dmoj
import leetcode
import spoj
import timus
import wcipeg
import genericExtractor as g1
import genericExtractor2 as g2

def extractor(page, domain, crawlerType, fileName):
    
    if domain == "A2oj":
        a2oj.a2oj(page, crawlerType, "Specific", domain, fileName)
    elif domain == "Codeforces":
        codeforces.codeforces(page, crawlerType, "Specific", domain, fileName)
    elif domain == "Dmoj":
        dmoj.dmoj(page, crawlerType, "Specific", domain, fileName)
    elif domain == "Leetcode":
        leetcode.leetcode(page, crawlerType, "Specific", domain, fileName)
    elif domain == "Spoj":
        spoj.spoj(page, crawlerType, "Specific", domain, fileName)
    elif domain == "Timus":
        timus.timus(page, crawlerType, "Specific", domain, fileName)
    elif domain == "Wcipeg":
        wcipeg.wcipeg(page, crawlerType, "Specific",domain,  fileName)
    
    g1.genericExtractor(page, crawlerType, "General", domain, fileName)
    g2.genericExtractor2(page, crawlerType, "General", domain, fileName)