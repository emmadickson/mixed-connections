import requests
import socks
import bs4
import hashlib
import re
import json
import datetime
import random
import os
from PIL import Image
import cStringIO
import psycopg2
import subprocess

# Constants
CRAIGSLIST_URLS = [
"https://newyork.craigslist.org",
"https://raleigh.craigslist.org",
"https://pittsburgh.craigslist.org"
]

NUMBER_OF_POSTS = 5
DATABASE_URL='postgres://pkszoedlaykwsk:2ff4fae6161d29c22cf40f349faaa1e48d8524aab1caf6eed72f773a31f0a91b@ec2-54-83-0-158.compute-1.amazonaws.com:5432/d42mu98rpmdqbj'
conn = psycopg2.connect(DATABASE_URL, sslmode='require', user='pkszoedlaykwsk', password='2ff4fae6161d29c22cf40f349faaa1e48d8524aab1caf6eed72f773a31f0a91b' )
cursor = conn.cursor()

def CollectMissedConnectionsLink(location):
    '''Returns a list of recent posts urls from the location specific missed
    connection url passed'''
    craigslistMissedConnectionsUrls = []
    randomCraigslistUrl = CRAIGSLIST_URLS[location] + "/search/mis"
    response = requests.get(randomCraigslistUrl).text
    soup = bs4.BeautifulSoup(response, "html.parser")
    for link in soup.findAll('a', href=True, text=''):
        if ('html' in link['href']):
            craigslistMissedConnectionsUrls.append( link['href'] )
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
    hashedPostBody = GetHash(body)
    # For debugging purposes

    print("Post from %s added" % location)
    print(body)
    return (title, body, location, str(today), str(hashedPostBody))

def ScrapeImages(finalUrl):
    '''Scrapes and shuffles all the images found in a post from the url passed'''
    images = []
    IMAGE_HASHES =  []
    response = requests.get(finalUrl).text
    soup = bs4.BeautifulSoup(response, "html.parser")
    for link in soup.findAll('a', href=True, text=''):
            if ('images' in link['href']):
                images.append( link['href'] )
    for img in soup.findAll('img'):
        images.append(img['src'])

    scraped_images = os.listdir("static/images/scraped_images")
    random.shuffle(scraped_images)
    opened_images = []

    for x in range(0, len(scraped_images)):
        opened_images.append(Image.open("static/images/scraped_images/%s.jpg" % x))

    for x in range(0, len(scraped_images)-1):
        os.remove("static/images/scraped_images/%s.jpg" % x)

    for x in range(0, len(opened_images)):
        opened_images[x].save(("static/images/scraped_images/%s" % scraped_images[x]), "JPEG")

    image_number = len(scraped_images)
    for img in images:
        if ("50x50" not in img) and img not in IMAGE_HASHES:
            file = cStringIO.StringIO(urllib2.urlopen(img).read())
            img = Image.open(file)
            image_number = image_number + 1
            img.save("static/images/scraped_images/%s.jpg" % image_number, "JPEG")
            print "image saved!"

def main():

    # 4. Pick a random location, scrape recent posts and chose one to add
    for x in range(0, NUMBER_OF_POSTS):

        # 5. Pick a location randomly
        randomLocationUrl = random.randint(0,2)

        # 6. Collect regional Missed Connections posts linkToVisit
        craigslistMissedConnectionsUrls = CollectMissedConnectionsLink(randomLocationUrl)

        # 7. Shuffle the collected links to randomize selection
        random.shuffle(craigslistMissedConnectionsUrls)

        # 8. Get Missed Connections post body from the new links
        craigslistMissedConnectionsUrls = CollectMissedConnectionsLink(randomLocationUrl)

        # 9. Get a random number and use it to select the post to be added
        randomPostUrl = random.randint(0,len(craigslistMissedConnectionsUrls)-1)
        finalUrl = craigslistMissedConnectionsUrls[randomPostUrl]

        # 12. Check if it's already in the store, if not add it and scrape any images found in it
        pageContent = GetPageContent(finalUrl)

        data = GetQueryData(pageContent, finalUrl, randomLocationUrl)

        query =  "INSERT INTO posts_scraped (body,time, hash, location, title) VALUES (%s, %s, %s, %s, %s);"
        try:
            cursor.execute(query, data)
            print("Post has been added to the database")
        except:
            print("Post is already in the database")
        ScrapeImages(finalUrl)

    subprocess.call('static/bash/gif_script.sh')
    return


main()
print("\n\n Done")
