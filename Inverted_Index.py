#Importing Libraries
import json
import os
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk import word_tokenize


#Stop words needed to remove from indexing
strStopWords = set(stopwords.words('english'))
strStopWords = strStopWords.union(",","(",")","[","]","{","}","#","@","!",":",".", ";")
ssStemmer = SnowballStemmer('english')
#Initiating empty directories
dictionary = {}
profinfo = {}
base_path = os.getcwd()

def InvertedIndexGenerator(strToken, URL):
    if strToken not in dictionary:
        dictionary[strToken] = [URL]
    elif strToken in dictionary:
        if URL not in dictionary[strToken]:
            dictionary[strToken].append(URL)


#preprosessing data by tokenizing, stamming and removing stop words
def tokenizer(strText, URL):
    strWords = word_tokenize(strText)
    for strWord in strWords:
        token = ssStemmer.stem(strWord)
        if token not in strStopWords:
            InvertedIndexGenerator(token,URL)


#Indexing preprocessed data
def TokenizeWebPageData(strJSONFile):
    #Loading json file of crawled data
    with open(strJSONFile,"r") as read_file:
        data = json.load(read_file)
        #Indexing all data against URL
        for i in range(0,len(data['lstProfessorURL'])):
            #Tokenise Name
            tokenizer(data['lstProfessorName'][i],data['lstProfessorURL'][i])

            #Tokenise Title
            tokenizer(data['lstProfessorTitle'][i],data['lstProfessorURL'][i])

            #Tokenise Contact details
            tokenizer(data['lstProfessorContact'][i],data['lstProfessorURL'][i])

            #Tokenise Profile
            tokenizer(data['lstProfessor_profile'][i],data['lstProfessorURL'][i])

            #Tokenise Fingerprint
            tokenizer(data['lstProfessor_fingerprint'][i],data['lstProfessorURL'][i])
            #print(data['lstProfessorName'][i] + " : " + data['lstProfessorURL'][i])

            #Append professor information for search result display
            if data['lstProfessorURL'][i] not in profinfo:
                profinfo[data['lstProfessorURL'][i]] = [data['lstProfessorName'][i]]
                profinfo[data['lstProfessorURL'][i]].append(data['lstProfessorTitle'][i])
                profinfo[data['lstProfessorURL'][i]].append(data['lstProfessorContact'][i])
                profinfo[data['lstProfessorURL'][i]].append(data['lstProfessor_profile'][i])
                profinfo[data['lstProfessorURL'][i]].append(data['lstProfessor_fingerprint'][i])


cov_json_file_path = base_path+'\\Web_scrap_data\\coventry.json'
ww_json_file_path = base_path+'\\Web_scrap_data\\warwick.json'
ip_json_file_path = base_path+'\\Web_scrap_data\\imperical.json'

#Tokenise data from all the 3 web scrapping
TokenizeWebPageData(ww_json_file_path)
TokenizeWebPageData(cov_json_file_path)
TokenizeWebPageData(ip_json_file_path)


tok_json_file_path = base_path+'\\Web_scrap_data\\tokenisedindex.json'
prof_json_file_path = base_path+'\\Web_scrap_data\\professorinfo.json'

#Making json file where all other data as key and URL as value
with open(tok_json_file_path, 'w') as fp:
    json.dump(dictionary, fp)
#Making json file where URL is key and all other data as value
with open(prof_json_file_path, 'w') as fpinfo:
    json.dump(profinfo, fpinfo)
