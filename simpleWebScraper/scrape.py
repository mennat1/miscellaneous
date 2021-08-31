# pip3 install lxml, requests, beatifulsoup4

import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

jobs = []
companies = []
locations = []
skills = []
links = []
responsibilities = []

page_num = 0
jobs_limit = "0"

while True:
	page_url = f"https://wuzzuf.net/search/jobs/?a=spbl&q=python&start={page_num}"
	# print(page_url)

	result = requests.get(page_url)
	# print(result)

	src = result.content
	# print(src)

	soup = BeautifulSoup(src, "lxml")
	# print(soup)

	jobs_limit = soup.find("div", {"class":"css-osele2"}).find("strong").text
	# print("Total Number Of Jobs Found = ", jobs_limit)

	job_titles = soup.find_all("h2", {"class":"css-m604qf"})
	# print(job_titles)

	company_names = soup.find_all("a", {"class":"css-17s97q8"})
	# print(company_names)

	locations_names = soup.find_all("span", {"class":"css-5wys0k"})
	# print(locations_names)

	job_skills = soup.find_all("div", {"class":"css-y4udm8"})
	# print(job_skills)


	for i in range(len(job_titles)):
		jobs.append(job_titles[i].text)
		companies.append(company_names[i].text)
		locations.append(locations_names[i].text)
		skills.append(job_skills[i].text)
		links.append(job_titles[i].find("a").attrs['href'])

	# print(jobs)
	# print(companies)
	# print(locations)
	# print(skills)
	# print(links)

	print("jobs scraped = ", len(jobs))
	if(len(jobs)==int(jobs_limit)):
		break
	page_num += 1
	print("switched page ", page_num)

print("DONE ++++++++++++++++++++++++++++++++")

for link in links:
	result = requests.get(link)
	src = result.content
	soup = BeautifulSoup(src, "lxml")
	responsibility = soup.find("div", {"class":"css-1uobp1k"})
	
	resp_text = ""
	if(responsibility.ul):
		for li in responsibility.ul.find_all("li"):
			resp_text += li.text + " || "
	resp_text = resp_text[:-3]
	responsibilities.append(resp_text)

file_list = [jobs, companies, locations, skills, responsibilities]
exported = zip_longest(*file_list)
print("NOW WE WILL WRITE TO THE CSV FILE ++++++++++++++++++++++++++++++++")
with open("jobs.csv", "w") as f:
	wr = csv.writer(f)
	wr.writerow(["Job Title", "Company Name", "Location", "Required Skills", "Responsibilities"])
	wr.writerows(exported)