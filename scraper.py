# We import the libraries we need
import requests # to connect the website we will scrape
import lxml.html as html # to extract and use the Xpath language
import os # for interacting with our pc
import datetime # to generate datetime variable
import pandas as pd

# The website we will scrape
HOME_URL = 'https://www.larepublica.co/'

# The Xpaths from where we will extract the info
XPATH_LINK_TO_ARTICLE = '//text-fill[not(@class)]/a/@href'
XPATH_TITLE = '//div[@class="mb-auto"]/h2/span/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p/text()'
XPATH_AUTHOR = '//div[@class = "author-article"]/div/button/text()'

# Function that will help us extract the data we want and save it in a directory
# also save it in lists to export them later as a csv file
title_list = []
author_list = []
summary_list = []
body_list = []

def parse_notice(link, today):



    try:
        # We request the website
        response = requests.get(link)

        # 200 means the website connected fine with the program
        if response.status_code == 200:

            # The website language is spanish so we decode it with  utf-8 for special
            # characters like "ñ","á","ó", and also we extract the content from the website
            notice = response.content.decode('utf-8')

            # We extract the website as a html file
            parsed = html.fromstring(notice)
            
            # We use 'try' in case of errors and parse the Xpaths in the places 
            # where we need info to extract it
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\n','')
                title = title.replace('\"','')
                title = title.replace("/",'')
                title = title.replace("?",'')
                title = title.replace(":",' -')
                title = title.strip()
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
                author = parsed.xpath(XPATH_AUTHOR)


                # We save info in the lists
                title_list.append(title)
                author_list.append(author)
                summary_list.append(summary)
                body_list.append(body)

            except IndexError:
                return

            # Saving it as a .txt file
            with open(f'{today}/{title}.txt','w',encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')

                # The author path output is a list so we iterate on it
                for a in author:
                    f.write(a)

                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')

                # The body is written in multiple paragraph
                for p in body:
                    f.write(p)
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

# Function to extract the urls from home LaRepublica page
def parse_home():
    
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            link_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            today = datetime.date.today().strftime("%d-%m-%Y")

            # Create a directory where the files will be save
            if not os.path.isdir(today):
                os.mkdir(today)

            # We iterate in each link we extracted and
            # run the previous function we created
            for link in link_to_notices:
                parse_notice(link, today)

            # Save lists on Dataframe and save it as a csv file
            pd.DataFrame(
                data={
                    'title':title_list,
                    'author(s)':author_list,
                    'summary':summary_list,
                    'body':body_list
                    }
                ).to_csv(f'CSVs\date-{today}.csv')

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == '__main__':
    run()