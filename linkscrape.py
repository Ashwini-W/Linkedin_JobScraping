from bs4 import BeautifulSoup as be
import requests
import csv
from datetime import datetime

time_='r604800' # 1 week time 
url='https://www.linkedin.com/jobs/search/?f_TPR={}'.format(time_) 
response = requests.get(url)
content = be(response.content, "html.parser")

csv_file = open('LinkedIn Jobs.csv','w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Job_title','Company name','Location','Post_Date'])

jobs_list_container = content.find('ul','jobs-search__results-list')


job_title = []
company_name = []
post_date = []
job_location=[]

import sqlite3
conn = sqlite3.connect('LinkInscrape.db')
curr=conn.cursor()

'''
curr.execute("""create table linkinjobst(
                job_title text,  
                Company_Name text,
                Location text,
                Post_date date
                )""") 
'''

for job in jobs_list_container:
    
    j_title = job.find("span", class_="screen-reader-text").text
    job_title.append(j_title)

    company_n = job.h4.text
    company_name.append(company_n)

    job_l = job.find("span", class_="job-result-card__location").text
    job_location.append(job_l)

    da = job.find('time')['datetime']
    oldformat=datetime.strptime(da,"%Y-%m-%d")
    date_=oldformat.strftime("%d-%m-%Y")
    post_date.append(date_)

    
    csv_writer.writerow([j_title,company_n,job_l,date_])
    '''
    curr.execute("""insert into linkinjobst values (?,?,?,?)""",(j_title,company_n,job_l,date_) )
    '''

'''
curr.execute("""Select * from linkinjobst""")
results = curr.fetchall()
print(results)
print(len(results))
'''

conn.commit()

csv_file.close()
conn.close()
