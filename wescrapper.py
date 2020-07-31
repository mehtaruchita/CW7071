#Importing Libraries
from reppy.robots import Robots
import coventry_uni_webscrap
import imperical_college_webScrap
import warwick_uni_Scrap
from coventry_uni_webscrap import cov_scrap
from imperical_college_webScrap import imperical_scrap
from warwick_uni_Scrap import warwick_scrap
import schedule


# 1. Scrap Coventry University website
cov_uni_link = 'https://www.coventry.ac.uk/research/areas-of-research/centre-for-data-science/our-team/'
cov_uni_robot = Robots.fetch('https://www.coventry.ac.uk/robots.txt')
#Checking robots.txt file if its allowed to crawl, it will call crawler function
blnCovScrap = cov_uni_robot.allowed(cov_uni_link, 'my-user-agent')
if blnCovScrap == True:
    cov_scrap(cov_uni_link)
schedule.every(7).days.do(lambda: cov_scrap(cov_uni_link))
while True:
    schedule.run_pending()



# 2. Scrap Imperical college website
imp_uni_link = 'https://www.imperial.ac.uk/data-science/about-the-institute/people/staff/'
imp_uni_robot = Robots.fetch('https://www.imperial.ac.uk/robots.txt')
#Checking robots.txt file if its allowed to crawl, it will call crawler function
blnImpScrap = imp_uni_robot.allowed(imp_uni_link, 'my-user-agent')
if blnImpScrap == True:
    imperical_scrap(imp_uni_link)
schedule.every(7).days.do(lambda: imperical_scrap(imp_uni_link))
while True:
    schedule.run_pending()


# 3. Scrap Warwick university website
wwk_uni_link = 'https://warwick.ac.uk/fac/sci/statistics/staff/academic-research'
wwk_uni_robot = Robots.fetch('https://warwick.ac.uk/robots.txt')
#Checking robots.txt file if its allowed to crawl, it will call crawler function
blnWwkScrap = wwk_uni_robot.allowed(wwk_uni_link, 'my-user-agent')
if blnWwkScrap == True:
    warwick_scrap(wwk_uni_link)
schedule.every(7).day.do(lambda: warwick_scrap(wwk_uni_link))
while True:
    schedule.run_pending()
