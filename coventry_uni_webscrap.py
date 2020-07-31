#Importing Libraries
import json
import time
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import os
base_path = os.getcwd()
#Function for coventry data science professors' list
def cov_scrap(weblink):
    sleep_interval = 5
    #Initiating Empty Lists
    lstProfessorName = []
    lstProfessorURL = []
    lstProfessorTitle = []
    lstProfessorContact = []
    lstProfessor_profile = []
    lstProfessor_fingerprint = []
    #Parsing webpage
    parsed_uri = urlparse(weblink)
    baseurl = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    req = Request(weblink, headers={'User-Agent': 'XYZ/3.0'})
    html_page = urlopen(req, timeout=10)
    soup = BeautifulSoup(html_page, "lxml")
    #Retrieving data from webpage
    researchteamtable = soup.find("table", attrs={"class": "table-grey-zebra"})
    researchteamdata = researchteamtable.tbody.find_all("tr")
    for i in range(1, len(researchteamdata)):
        t_row = []
        colno = 1
        for td in researchteamdata[i].find_all("td"):
            t_row.append(td.text.strip())
            if td.find("a") and colno == 2:
                profurl = td.find("a").get("href")
                profurl = profurl.strip()
            colno = colno + 1
        lstProfessorURL.append(profurl)
        lstProfessorName.append(t_row[1])
        lstProfessorTitle.append(t_row[2])
        lstProfessorContact.append(t_row[3])
        time.sleep(sleep_interval)
    #parsing professor's information page and fetching information from it
    for i in range(0, len(lstProfessorURL)):
        try:
            parse_profurl = urlparse(lstProfessorURL[i])
            req_profurl = Request(lstProfessorURL[i], headers={'User-Agent': 'XYZ/3.0'})
            html_page_prof = urlopen(req_profurl, timeout=10)
            print(html_page_prof)
            soup = BeautifulSoup(html_page_prof, "lxml")
            prof_profile_section = soup.find("section", attrs={
                "class": "page-section content-relation-section person-profileinformation"})
            prof_profile_text = prof_profile_section.text.strip()
            prof_fingerprint_section = soup.find("section", attrs={
                "class": "page-section content-relation-section person-fingerprint"})
            prof_profile_fingerpt = prof_fingerprint_section.find_all("span", attrs={"class": "concept"})
            prof_fingerprints = ""
            for fingerprint in prof_profile_fingerpt:
                if prof_fingerprints == "":
                    prof_fingerprints = fingerprint.text.strip()
                else:
                    prof_fingerprints = prof_fingerprints + "," + fingerprint.text.strip()
            print(prof_fingerprints)
            lstProfessor_profile.append(prof_profile_text)
            lstProfessor_fingerprint.append(prof_fingerprints)
            time.sleep(sleep_interval)
            print('-----------------------------------------')
        except:
            print('Could not find page:', lstProfessorURL[i])
            lstProfessor_profile.append("")
            lstProfessor_fingerprint.append("")
    #Printing all 6 lists
    print(*lstProfessorName, sep="\n")
    print(*lstProfessorTitle, sep="\n")
    print(*lstProfessorContact, sep="\n")
    print(*lstProfessorURL, sep="\n")
    print(*lstProfessor_profile, sep="\n")
    print(*lstProfessor_fingerprint, sep="\n")
    #List of lists
    lists_imp = ['lstProfessorName', 'lstProfessorTitle', 'lstProfessorContact', 'lstProfessorURL',
                 'lstProfessor_profile', 'lstProfessor_fingerprint']
    data = {}
    for keyname in lists_imp:
        data[keyname] = locals()[keyname]
    #Making json file for retrieved data from crawler
    json_file_path = base_path+'\\Web_scrap_data\\coventry.json'
    print("json file path: " + json_file_path)
    with open(json_file_path, 'w') as outfile:
        json.dump(data, outfile)


