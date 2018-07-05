import math
import sys
import itertools
import json
from Indexer.Text_Processing import pre_processing
from Indexer import util

# function that returns the tdidf weight of a document
def weightFileTDIDF(word, text, invertedFile, fileTotalNumber, fileRecoveredNumber):
    tf = len(invertedFile.get(word,[]))
    idf = 0
    try:
        idf = math.log(fileTotalNumber/fileRecoveredNumber,10)
    except:
        pass
    tfidf = tf*idf
    return tfidf
    
def weightFileBoolean(word, text, invertedFile, fileTotalNumber, fileRecoveredNumber):
    tf = len(invertedFile.get(word,[]))
    if(tf>0):
        return 1
    return 0

# function that returns a vector of a document based on a query.
# a query with duplicate elements will remove the duplicates to build the vector
# example query = ["cat","bad","cat","bad"] will return a vector with two elements like [0.30102999566398114, 0.15051499783199057]
# because the second "cat" and the second "bad" will be eliminated
def vectorFile(query, text, invertedFile, fileTotalNumber, fileRecoveredNumber, boolean):
    result = []
    query = removeDuplicates(query)
    for q in query:
        if(boolean):
            result.append(weightFileBoolean(q, text, invertedFile, fileTotalNumber, fileRecoveredNumber))
        else:
            result.append(weightFileTDIDF(q, text, invertedFile, fileTotalNumber, fileRecoveredNumber))
    return result
 
# function that returns the tdidf weight of a query
def weightQueryTDIDF(word, query, fileTotalNumber, fileRecoveredNumber):
    tf = query.count(word)/float(len(query))
    idf = 0
    try:
        idf = math.log(fileTotalNumber/fileRecoveredNumber,10)
    except:
        pass
    tfidf = tf*idf
    return tfidf
    
def weightQueryBoolean(word, query, fileTotalNumber, fileRecoveredNumber):
    tf = query.count(word)/float(len(query))
    if(tf>0):
        return 1
    return 0

# function that returns a vector of a query
# a query with duplicate elements will remove the duplicates to build the vector
# example query = ["cat","bad","cat","bad"] will return a vector with two elements like [0.30102999566398114, 0.30102999566398114]
# because the second "cat" and the second "bad" will be eliminated  
def vectorQuery(query, fileTotalNumber, fileRecoveredNumber, boolean):
    result = []
    queryM = removeDuplicates(query)
    for q in queryM:
        if(boolean):
            result.append(weightQueryBoolean(q, query, fileTotalNumber, fileRecoveredNumber))
        else:
            result.append(weightQueryTDIDF(q, query, fileTotalNumber, fileRecoveredNumber))
    return result
    
# function that eliminate the duplicates of a query
def removeDuplicates(query):
    result = []
    for q in query:
       if q not in result:
           result.append(q)
    return result

# function that calculates the cossine between two vectors
# It was did because I needed to use Vector Space Model to do my tests
def cos(vector1, vector2):
    l = range(0,len(vector1))
    num = 0
    for i in l:
        num += (vector1[i] * vector2[i])
    v1 = map(lambda x: x ** 2, vector1)
    v2 = map(lambda x: x ** 2, vector2)
    x1 = sum(v1)
    x2 = sum(v2)
    x1 = math.sqrt(x1)
    x2 = math.sqrt(x2)
    den = x1*x2
    if den == 0:
        return 0
    return num/den

###############################################################################
# here is a method using term proximity thought by Valdemiro. I didn't find any 
# place that do the same. Maybe there is but not sure
# Based in a method that uses Vector Space Model and Term Proximity and 
# calculates a matrix with distance between terms
# I thought that do the sum between this distances could be a nice heuristic
# that returns a good result (need to be validated)
# It is important to say that here uses Vector Space Model to calculate the relecance too,
# when the weight of term proximity is the same

# function that calculates the minimun distance between two terms in a doc
def minDist(term1, term2, invertedFile):
    if len(invertedFile.get(term1,[])) == 0:
        return 150000
    if len(invertedFile.get(term2,[])) == 0:
        return 150000
    minValue = 150000
    list1 = invertedFile.get(term1)
    list2 = invertedFile.get(term2)
    l1 = range(0,len(list1))
    l2 = range(0,len(list2))
    for i in l1:
        for j in l2:
            if(abs(list2[j]-list1[i])<minValue):
                minValue = abs(list2[j]-list1[i])
    return minValue

#function that calculates the minimum distance between all terms of the query
# and stores in a two-dimensional list
def matrixDist(query, invertedFile):
    query = removeDuplicates(query)
    matrix = [[0 for x in range(len(query))] for y in range(len(query))]
    l1 = range(0,len(query))
    for i in l1:
        for j in l1:
            if i!=j:
                matrix[i][j] = minDist(query[i],query[j],invertedFile)
    return matrix

#function that do the sum of all distances
def weightFileTermProximity(query, invertedFile):
    if(len(query)==1):
        l1 = invertedFile.get(query[0],[])
        if(len(l1)==0):
            return sys.float_info.max
        else:
            return 1/len(l1)
    return (float)(sum(map(sum, matrixDist(query, invertedFile)))/2)

#function that receive a query, a doc list, a inverted file list, the total
# number of all documents that exists in database, and the total number
# of files that were recovered and returns a pair list of weight and docs
# in relevance order
def rankingDocsaux(query, docs, invertedFiles, fileTotalNumber, pair):
    fileRecoveredNumber = len(docs)
    length =  range(0,len(docs))
    vecQuery = vectorQuery(query,fileTotalNumber, fileRecoveredNumber, False)
    for i in length:
        termProx = weightFileTermProximity(query, invertedFiles[i])
        vect = -(cos(vecQuery, vectorFile(query, docs[i], invertedFiles[i],fileTotalNumber, fileRecoveredNumber,False)))
        if pair[i][0]>termProx:
            pair[i] = [termProx, vect, docs[i]]
        elif (pair[i][0]==termProx) and (pair[i][1]>vect):
            pair[i] = [termProx, vect, docs[i]]
    pair = sorted(pair)
    return pair
    
def rankingDocsaux1(query, docs, invertedFiles, fileTotalNumber, pair, boolean):
    fileRecoveredNumber = len(docs)
    length =  range(0,len(docs))
    vecQuery = vectorQuery(query,fileTotalNumber, fileRecoveredNumber, boolean)
    for i in length:
        termProx = 0
        vect = -(cos(vecQuery, vectorFile(query, docs[i], invertedFiles[i],fileTotalNumber, fileRecoveredNumber, boolean)))
        if pair[i][0]>termProx:
            pair[i] = [termProx, vect, docs[i]]
        elif (pair[i][0]==termProx) and (pair[i][1]>vect):
            pair[i] = [termProx, vect, docs[i]]
    pair = sorted(pair)
    return pair

# Ranking that uses term proximity and vector space model
def rankingDocs(query, docs, invertedFiles, fileTotalNumber, space = False, boolean = False):
    pair = [[999999999.0,0.0,docs[0]] for x in range(len(docs))]
    if(space):
        pair = rankingDocsaux1(query, docs, invertedFiles, fileTotalNumber, pair, boolean)
    else:
        pair = rankingDocsaux(query, docs, invertedFiles, fileTotalNumber, pair)
    return pair



def getInvertedFile(typeInverted, typeQuery):
    file = 'Indexer/Files/Inverted/' + typeInverted + '/nCompressed/' +typeQuery
    datas = {}
    with open(file) as f:
        datas = json.load(f)
    return datas

def countTotalDocs():
    file = 'Docs/Jsons/Heuristic2/Specific/'
    value = 0
    for a in ['A2oj/a2oj.json', 'Codeforces/codeforces.json', 'Spoj/spoj.json', 'Timus/timus.json', 'Wcipeg/wcipeg.json']:
        datas = {}
        with open(file+a) as f:
            datas = json.load(f)
            value += len(datas.keys())
    return value

def rankingGeneral (query, invertedFile, fileTotalNumber ,space = False, boolean = False):
    q = removeDuplicates(query)
    docsID = set()
    for e in q:
        for v in invertedFile.get(e,[]):
            docsID.add(v[0])
    docs = []
    for e in docsID:
        docs.append(e)
    docsID = []
    docsID = docs
    #print(docsID)
    invertedFileDocs = {}
    for d in docsID:
        invertedFileDocs[d] = {}
    for e in q:
        for v in invertedFile.get(e,[]):
            invertedFileDocs[v[0]][e] = v[2]
    aux = invertedFileDocs
    invertedFileDocs = []
    for e in docs:
        invertedFileDocs.append(aux[e])
    rank = rankingDocs(query,docsID, invertedFileDocs, fileTotalNumber, space, boolean)
    return rank
   
# python3 -m nltk.downloader stopwords
# python3 -m nltk.downloader punkt
  
invertedFileDescription = getInvertedFile('Positional', 'description')
invertedFileInput = getInvertedFile('Positional', 'input')
invertedFileOutput = getInvertedFile('Positional', 'output')
invertedFileTimeLimit= getInvertedFile('Positional', 'time limit')
invertedFileTitle = getInvertedFile('Positional', 'title')
invertedFileProblem = getInvertedFile('Positional', 'problem')
    
def ranking(description, inputDescription, outputDescription, timeLimit, title, problem, space = False, boolean = False):
    cont = countTotalDocs()
    qDescription = pre_processing.processData(description)
    qInput = pre_processing.processData(inputDescription)
    qOutput = pre_processing.processData(outputDescription)
    aux = pre_processing.processTimeL(timeLimit)
    qTimeLimit = []
    for a in aux:
        try:
            float(a)
            qTimeLimit.append(a)
        except:
            pass
    
    aux = qTimeLimit
    qTimeLimit = []
    for a in aux:
        qTimeLimit.append(util.searchRange(invertedFileTimeLimit.keys(), a))
    qTitle = pre_processing.processData(title)
    qProblem = pre_processing.processData(problem)
    ans = {}
    value = 0
    if(qDescription!=[]):
        value += 1
        rank = rankingGeneral(qDescription, invertedFileDescription, cont, space, boolean)
        for r in rank:
            if(ans.get(r[2],[])==[]):
                ans[r[2]] = []
            ans[r[2]].append(r)
    if(qInput!=[]):
        value += 1
        rank = rankingGeneral(qInput, invertedFileInput, cont, space, boolean)
        for r in rank:
            if(ans.get(r[2],[])==[]):
                ans[r[2]] = []
            ans[r[2]].append(r)   
    if(qOutput!=[]):
        value += 1
        rank = rankingGeneral(qOutput, invertedFileOutput, cont, space, boolean)
        for r in rank:
            if(ans.get(r[2],[])==[]):
                ans[r[2]] = []
            ans[r[2]].append(r)
    if(qTimeLimit!=[]):
        value += 1
        rank = rankingGeneral(qTimeLimit, invertedFileTimeLimit, cont, space, boolean)
        for r in rank:
            if(ans.get(r[2],[])==[]):
                ans[r[2]] = []
            ans[r[2]].append(r)       
    if(qTitle!=[]):
        value += 1
        rank = rankingGeneral(qTitle, invertedFileTitle, cont, space, boolean)
        for r in rank:
            if(ans.get(r[2],[])==[]):
                ans[r[2]] = []
            ans[r[2]].append(r)
    if(qProblem!=[]):
        value += 1
        rank = rankingGeneral(qProblem, invertedFileProblem, cont, space, boolean)
        for r in rank:
            if(ans.get(r[2],[])==[]):
                ans[r[2]] = []
            ans[r[2]].append(r)
    aux = ans
    ans = []
    for k in aux.keys():
        if(len(aux[k])==value):
            i = [0.0,0.0, 0]
            for v in aux[k]:
                i[0] += v[0]
                i[1] += v[1]
                i[2] = v[2]
            i[0] /= value
            i[1] /= value
            ans.append(i)
    ans = sorted(ans)
    rankedDocs = []
    for a in ans:
        rankedDocs.append(a[2])
    return rankedDocs
    


def spearman(query):
    rank1 = ranking('','','','','',query,True,False)
    table = {}
    for i in range(0,len(rank1)):
        table[rank1[i]] = []
        table[rank1[i]].append(i)
    rank2 = ranking('','','','','',query,False,False)
    for i in range(0,len(rank2)):
        table[rank2[i]].append(i)
    sumSquares = 0.0
    for k in table.keys():
        sumSquares += ((table[k][0]-table[k][1])*(table[k][0]-table[k][1]))
    sumSquares *= 6.0
    k = len(rank1)
    den = k*((k*k)-1)
    ans = 1 - (sumSquares/den)
    return ans

def kendal(query):
    rank1 = ranking('','','','','',query,True,False)
    rank2 = ranking('','','','','',query,False,False)
    p = {}
    for i in range(0,len(rank1)):
        for j in range(i+1, len(rank1)):
            if p.get((rank1[i],rank1[j]),-1) == -1:
                p[(rank1[i],rank1[j])] = 0
            p[(rank1[i],rank1[j])] += 1
            if p.get((rank2[i],rank2[j]),-1) == -1:
                p[(rank2[i],rank2[j])] = 0
            p[(rank2[i],rank2[j])] += 1
    dis = 0.0
    for k in p.keys():
        if(p[k]==1):
            dis += 1
    dis *= 2.0
    k = len(rank1)
    den = k*(k-1)
    ans = 1 - (dis/den)
    return ans

c1 = 'Graph Search'
c2 = 'Fibonacci Sum'
c3 = 'Dynamic Programming'
c4 = 'Card Game'
c5 = 'Bit Manipulation'

'''
print("Spearman: ")
print(c1+ ": "+str(spearman(c1)))
print(c2+ ": "+str(spearman(c2)))
print(c3+ ": "+str(spearman(c3)))
print(c4+ ": "+str(spearman(c4)))
print(c5+ ": "+str(spearman(c5)))
print("Kendal Tau: ")
print(c1+ ": "+str(kendal(c1)))
print(c2+ ": "+str(kendal(c2)))
print(c3+ ": "+str(kendal(c3)))
print(c4+ ": "+str(kendal(c4)))
print(c5+ ": "+str(kendal(c5)))
'''

