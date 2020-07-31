#Importing Libraries
from bs4 import BeautifulSoup
import json
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import time
import os

base_path = os.getcwd()
def imperical_scrap(weblink):
    sleep_interval = 5
    present = True
    #Initializing Empty Lists
    lstProfessorName = []
    lstProfessorURL = []
    lstProfessorTitle = []
    lstProfessorContact = []
    lstProfessor_profile = []
    lstProfessor_fingerprint = []
    #Parsing and crawling data
    parsed_uri = urlparse(weblink)
    req = Request(weblink, headers={'User-Agent': 'XYZ/3.0'})
    html_page = urlopen(req, timeout=10)
    print(html_page)
    soup = BeautifulSoup(html_page, "lxml")
    staff_class = soup.find("ul", attrs={"class": "people list"})
    staff_name_list = staff_class.find_all("h3", attrs={"class": "sr-only"})
    staff_url_class = staff_class.find_all("a", attrs={"class": "name-link"})
    staff_title_list = staff_class.find_all("span", attrs={"class": "job-title"})
    staff_contact_list = staff_class.find_all("a", attrs={"class": "email"})
    for i in range(0, len(staff_name_list)):
        lstProfessorName.append(staff_name_list[i].text.strip())
        lstProfessorURL.append(staff_url_class[i].get("href").strip())
        lstProfessorTitle.append(staff_title_list[i].text.strip())
        mail_id = (staff_contact_list[i].get("href").strip())
        lstProfessorContact.append(mail_id.replace("mailto:", ""))
        time.sleep(sleep_interval)
    print(*lstProfessorName, sep='\n')
    print(*lstProfessorURL, sep='\n')
    print(*lstProfessorTitle, sep='\n')
    print(*lstProfessorContact, sep='\n')
    #Crawling personal page of each professor
    for i in range(len(lstProfessorURL)):
        try:
            #parse_profurl = urlparse(lst_professor_url[i])
            req_prof_url = Request(lstProfessorURL[i], headers={'User-Agent': 'XYZ/3.0'})
            html_page_prof = urlopen(req_prof_url, timeout=10)
            soup = BeautifulSoup(html_page_prof, "lxml")
            prof_profile_div = soup.find("div", attrs={"class": "contentAndSidebar"})
            prof_profile_info = prof_profile_div.find("div", attrs={"id": "customContent"})
            prof_profile_info_text = prof_profile_info.text.strip()
            prof_profile_fingerprint_ul = soup.find("ul", attrs={"class": "linklist"})
            prof_profile_fingerprint = prof_profile_fingerprint_ul.find_all("li")
            prof_fingerprints = ""
            for fingerprint in prof_profile_fingerprint:
                if prof_fingerprints == "":
                    prof_fingerprints = fingerprint.text.strip()
                else:
                    prof_fingerprints = prof_fingerprints + "," + fingerprint.text.strip()
            lstProfessor_profile.append(prof_profile_info_text)
            lstProfessor_fingerprint.append(prof_fingerprints)
            time.sleep(sleep_interval)
        except:
            print('Could not find page:', lstProfessorURL[i])
            lstProfessor_profile.append("")
            lstProfessor_fingerprint.append("")
            time.sleep(sleep_interval)
    #Making list of liss
    lists_imp = ['lstProfessorName', 'lstProfessorTitle', 'lstProfessorContact', 'lstProfessorURL', 'lstProfessor_profile', 'lstProfessor_fingerprint']
    data = {}
    for keyname in lists_imp:
        data[keyname] = locals()[keyname]
    #making json file of crawled data
    json_file_path = base_path+'\\Web_scrap_data\\imperical.json'
    print("json file path: " + json_file_path)
    with open(json_file_path, 'w') as outfile:
        json.dump(data, outfile)
