import requests
import pandas as pd
import numpy as np
from requests import get
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

from time import sleep
from random import randint

companyName = []
headquarters = []
reviews = []
salaries = []
interviews = []
websites = []
ratings = []

no_pages = 100 # Number pages you want to scrap 

for page in range(1, no_pages + 1):

    if page == 1:
        url = "https://www.glassdoor.co.in/Reviews/india-reviews-SRCH_IL.0,5_IN115.htm"
        req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, "html.parser")
        company_div = soup.find_all('div', class_='single-company-result module')
    else:
        url = f"https://www.glassdoor.co.in/Reviews/india-reviews-SRCH_IL.0,5_IN115_IP{page}.htm"
        req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, "html.parser")
        company_div = soup.find_all('div', class_='single-company-result module')

    for container in company_div:
        
        #Company Name
        try:
            name = container.h2.a.text
            companyName.append(name)
        except:
            companyName.append("")


        #Ratings on glassdoor
        try:
            rating = container.h2.find('span', class_='bigRating strong margRtSm h2').text
            ratings.append(rating)
        except:
            ratings.append("")

        # Headquarters
        try:
            headquarter = container.p.find('span', class_='value').text
            headquarters.append(headquarter)
        except:
            headquarters.append("")

        try:
        # websites
            website = container.find('p', class_='webInfo mb-0 mt-xxsm').find("a").text
            websites.append(website)
        except:
            websites.append("")

        # No. of reviews
        try:
            review = container.find('div', class_='ei-contribution-wrap col-4 pl-lg-0 pr-0').find('span', class_='num h2').text
            reviews.append(review)
        except:
            reviews.append("")

        # Average salary
        try:
            salary = container.find('div', class_='ei-contribution-wrap col-4 p-0').find('span', class_='num h2').text
            salaries.append(salary)
        except:
            salaries.append("")

        # Number of interviews
        try:
            interview = container.find('div', class_='ei-contribution-wrap col-4 pl-0').find('span', class_='num h2').text
            interviews.append(interview)
        except:
            interviews.append("")
        
    """
    Controlling the crawl rate is beneficial for the
    scraper and for the website we’re scraping. If we 
    avoid hammering the server with a lot of requests 
    all at once, then we’re much less likely to get 
    our IP address banned — and we also avoid disrupting
    the activity of the website we scrape by allowing 
    the server to respond to other user requests as well.
    """
    sleep(randint(2,10))  # function will vary the amount of waiting time between requests for a number between 2-10 seconds.

    
companies = pd.DataFrame({
    'Company Name': companyName,
    'Headquarters': headquarters,
    'Website': websites,
    'Ratings': ratings,
    'Average Salary': salaries,
    'No. of Reviews': reviews,
    'No. of Interviews': interviews,
})

print(companies)

# to see the datatypes of your columns
print(companies.dtypes)

# Check missing data:
print(companies.isnull().sum())


#Add default value for missing data:
companies.Headquarters = companies.Headquarters.fillna("None Given")
companies.Website = companies.Website.fillna("None Given")
companies.Ratings = companies.Ratings.fillna(0.0)

companies.to_csv('companies.csv', index=False)
