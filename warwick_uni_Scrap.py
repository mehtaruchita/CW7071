# Importing Libraries
import json
import time
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import os
base_path = os.getcwd()
def warwick_scrap(weblink):
    sleep_interval = 5
    #Initializing empty lists
    lstProfessorName = []
    lstProfessorURL = []
    lstProfessorTitle = []
    lstProfessorContact = []
    lstProfessor_profile = []
    lstProfessor_fingerprint = []
    #Parcing and crawling web page
    parsed_uri = urlparse(weblink)
    baseurl = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    req = Request(weblink, headers={'User-Agent': 'XYZ/3.0'})
    html_page = urlopen(req, timeout=10)
    print(html_page)
    soup = BeautifulSoup(html_page, "lxml")
    prof_name_table = soup.find("table", attrs={"class": "table"})
    prof_name_tr = prof_name_table.find_all("tr")
    # prof_fingerprint = prof_name_tr.find("td", attr={"style":"height: 77px; width: 74%;"}).text.strip()
    for i in range(0, len(prof_name_tr)):
        try:
            prof_details_td = prof_name_tr[i].find_all("td")
            prof_name = prof_details_td[0].text.strip()
            prof_url = prof_details_td[0].find("a").get("href").strip()
            prof_fingerprint = prof_details_td[2].text.strip()
            lstProfessorName.append(prof_name)
            lstProfessorURL.append(prof_url)
            lstProfessor_fingerprint.append(prof_fingerprint)
            lstProfessorTitle.append("")

            time.sleep(sleep_interval)
        except:
            lstProfessorName.append("")
            lstProfessorURL.append("")
            lstProfessor_fingerprint.append("")
            lstProfessorTitle.append("")

    print(*lstProfessorName, sep="\n")
    print(*lstProfessorURL, sep="\n")
    print(*lstProfessor_fingerprint, sep="\n")
    #Crawling personal page of each Professor's web page
    for i in range(len(lstProfessorURL)):
        try:
            parse_profurl = urlparse(lstProfessorURL[i])
            req_profurl = Request(lstProfessorURL[i], headers={'User-Agent': 'XYZ/3.0'})
            html_page_prof = urlopen(req_profurl, timeout=10)
            soup = BeautifulSoup(html_page_prof, "lxml")
            prof_profile_div = soup.find("div", attrs={"class": "column-1-content"})
            prof_profile = prof_profile_div.text.strip()
            prof_cont_div = soup.find("div", attrs={"class": "column-2-content"})
            lstProfessorContact.append("")
            lstProfessor_profile.append(prof_profile)
            time.sleep(sleep_interval)
        except:
            lstProfessor_profile.append("")
            lstProfessorContact.append("")
    print(*lstProfessor_profile, sep="\n")
    lists_war = ['lstProfessorName', 'lstProfessorTitle', 'lstProfessorContact', 'lstProfessorURL',
                 'lstProfessor_profile', 'lstProfessor_fingerprint']
    data = {}
    for keyname in lists_war:
        data[keyname] = locals()[keyname]
    #Making a json file for crawled data
    json_file_path = base_path+'\\Web_scrap_data\\warwick.json'
    print("json file path: " + json_file_path)
    with open(json_file_path, 'w') as outfile:
        json.dump(data, outfile)
