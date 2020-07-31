#Importing Libraries
import json
import re
from functools import reduce
import rank_bm25
from rank_bm25 import BM25Okapi
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import os

base_path = os.getcwd()

#Stop words which needs to remove from query
strStopWords = set(stopwords.words('english'))
strStopWords = strStopWords.union(",","(",")","[","]","{","}","#","@","!",":",".", ";")
ssStemmer = SnowballStemmer('english')
#Importing indexed json files
strIndexFile = base_path+'\\Web_scrap_data\\tokenisedindex.json'
strProfInfoFile = base_path+'\\Web_scrap_data\\professorinfo.json'

#cleaning query by tokenizing, stemming and removing stop words
def cleanquery(strQuery):
    p = re.compile("\w+")
    querywords = p.findall(strQuery)
    querywords = [word.lower() for word in querywords]
    querywords = [ssStemmer.stem(word) for word in querywords]
    querywords = [word for word in querywords if word not in strStopWords]
    return querywords

#fetching query result from indexed files
def queryresult(strQuery):
    queryWords = cleanquery(strQuery)
    try:
        searchresultsinfo = {}
        with open(strIndexFile, "r") as read_file:
            indexData = json.load(read_file)

        with open(strProfInfoFile, "r") as read_prof_file:
            profdata = json.load(read_prof_file)
        #Optimizing Query result
        results = [set(indexData[word]) for word in queryWords]
        results = reduce(lambda x, y: x & y, results) if results else []

        for result in results:
            if result not in searchresultsinfo:
                searchresultsinfo[result] = [profdata[result]]

        return searchresultsinfo
    except:
        return []
