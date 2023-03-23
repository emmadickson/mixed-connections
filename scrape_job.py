import bs4
import hashlib
import re
import datetime
import random
import pandas as pd
import sys
from retrieve_posts import retrieve_posts_csv
import os
import psycopg2
import boto3
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

# Constants
CRAIGSLIST_URLS = [
"https://newyork.craigslist.org",
"https://raleigh.craigslist.org",
"https://pittsburgh.craigslist.org",
"https://maine.craigslist.org"
]

NUMBER_OF_POSTS = int(sys.argv[1])
DATABASE_URL =  os.environ.get('DATABASE_URL')
ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.environ.get('AWS_SECRET_KEY')



def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    s3.upload_file(local_file, bucket, s3_file)
    print("Upload Successful")

def CollectMissedConnectionsLink(location):
    '''Returns a list of recent posts urls from the location specific missed
    connection url passed'''
    craigslistMissedConnectionsUrls = []
    randomCraigslistUrl = CRAIGSLIST_URLS[location] + "/search/mis"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)


    driver.get(randomCraigslistUrl)
    print(randomCraigslistUrl)
    content = driver.find_elements(By.CLASS_NAME, "cl-search-result")
    print(content)
    for elem in content:
        link = elem.find_element(By.TAG_NAME, "a")

        href = elem.get_attribute('href')
        if href is not None:
            craigslistMissedConnectionsUrls.append(href)
    print(craigslistMissedConnectionsUrls)
    return craigslistMissedConnectionsUrls

def GetTitle(pageContent):
    '''Returns the title of the passed page content'''
    title = pageContent.select('title')[0].get_text()
    title = Clean(title)
    return title

def GetLocation(randomLocationUrl):
    '''Scrape a readable location from the location specific missed connections
    url so that it can be displayed in the header'''
    location = CRAIGSLIST_URLS[randomLocationUrl]
    if ".org" in location:
        location = CRAIGSLIST_URLS[randomLocationUrl][8:-15]
    else:
        location = CRAIGSLIST_URLS[randomLocationUrl][8:-14]
    return location

def GetHash(postBody):
    '''Returns a hash of the post body passed to it'''
    hashObject = hashlib.md5(postBody)
    hashedPostBody = hashObject.hexdigest()
    return hashedPostBody;

def GetPageContent(linkToVisit):
    '''Returns the page content of the link passed to it'''
    response = requests.get(linkToVisit)
    pageContent = bs4.BeautifulSoup(response.text, "html.parser")
    return pageContent;

def GetBody(finalUrl):
    '''Returns the body of the post from the url passed to it. Dependent
    upon the structure of the craiglist page'''
    print(f"finalUrl {finalUrl}")
    pageContent = GetPageContent(finalUrl)
    body = pageContent.select('section#postingbody')[0].get_text()
    body = body.split("QR Code Link to This Post")[1]
    body = Clean(body)
    return body

def Clean(content):
    ''''Returns a slightly styled version of the content passed to it'''
    content = re.sub('\n', '', content)
    content = (content).replace('"', "'")
    content = content.rstrip()
    content = content.encode('utf-8')
    return content

def GetQueryData(pageContent, finalUrl, randomLocationUrl):
    '''Returns a json compliant post'''
    title = GetTitle(pageContent)
    today = datetime.date.today()
    location = GetLocation(randomLocationUrl)
    body = GetBody(finalUrl)
    hashedPost = GetHash(body)
    # For debugging purposes

    print("Post from %s fetched" % location)
    print(body)
    return (title.decode('utf-8'), body.decode('utf-8'), str(location), str(today), str(hashedPost))

def main():

    #   4. Pick a random location, scrape recent posts and chose one to add
    for x in range(0, NUMBER_OF_POSTS):

        # 5. Pick a location randomly
        randomLocationUrl = random.randint(0,3)

        # 6. Collect regional Missed Connections posts linkToVisit
        craigslistMissedConnectionsUrls = CollectMissedConnectionsLink(randomLocationUrl)

        # 7. Shuffle the collected links to randomize selection
        random.shuffle(craigslistMissedConnectionsUrls)


        # 9. Get a random number and use it to select the post to be added
        number_of_posts = len(craigslistMissedConnectionsUrls)
        print(f"number_of_posts {number_of_posts} found for location {randomLocationUrl}")

        if number_of_posts == 0:
            return

        randomPostUrl = random.randint(1,number_of_posts)

        finalUrl = craigslistMissedConnectionsUrls[randomPostUrl]

        # 12. Check if it's already in the store, if not add it and scrape any images found in it
        pageContent = GetPageContent(finalUrl)

        data = GetQueryData(pageContent, finalUrl, randomLocationUrl)

        query =  "INSERT INTO posts_scraped (title, body, location, time, hash) VALUES (%s, %s, %s, %s, %s);"
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            t = cursor.execute(query, data)
            conn.commit()
            cursor.close()
            conn.close()
            print("Post has been added to the database\n")
        except Exception as e:
            print("Error %s" % e)
            continue

    csv = retrieve_posts_csv()
    csv_file = open(f'output_{datetime.date.today()}.csv', 'w')
    csv_file.write(csv)
    csv_file.close()
    upload_to_aws('output.csv', 'mixed-connections', 'output.csv')



    return


main()
print("Done Scraping")
