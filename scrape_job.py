from flask import request
import requests
import socks
import socket
import bs4
import hashlib
import re
import json
import datetime
from random import shuffle
import random
import os
from PIL import Image
import urllib2
import cStringIO
import subprocess
import time
import glob

# Constants
CRAIGSLIST_URLS = [
"https://newyork.craigslist.org",
"https://raleigh.craigslist.org",
"https://pittsburgh.craigslist.org"
]

NUMBER_OF_POSTS = 5
DB_FILE = "static/data/db.json"
ENTRIES_FILE = "static/data/db.json"


def CollectEntriesHashes(entries):
    '''Returns a list of hashes from the post body of the entries passed'''
    hashes = []
    for entry in entries:
        hash = entry['hash']
        hashes.append(hash)
    return hashes

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

def HashExists(hashedPostBody, hashes):
    '''Checks if the hash exists in the collected hashes'''
    if (hashedPostBody not in hashes):
        return True
    else:
        return False

def CreateEntry(pageContent, finalUrl, randomLocationUrl):
    '''Returns a json compliant post'''
    title = GetTitle(pageContent)
    today = datetime.date.today()
    location = GetLocation(randomLocationUrl)
    body = GetBody(finalUrl)
    hashedPostBody = GetHash(body)
    # For debugging purposes
    print("Post from %s added" % location)
    dbEntry = "{ \"title\": \"%s\" , \"body\": \"%s\", \"location\": \"%s\", \"time\": \"%s\", \"hash\":\"%s\"}"  % (title, body, location, str(today), str(hashedPostBody))
    return dbEntry

def WriteStoreToFile(file, storedEntries):
    '''Writes a list of passed entries to the passed file'''
    textEntries = open(file, 'w')
    textEntries.write("{\"posts\":[")
    for x in range(0, len(storedEntries)-2):
        if (storedEntries[x] != None and len(storedEntries[x]) > 2):
            textEntries.write(str(storedEntries[x]))
            textEntries.write(",")
    textEntries.write(storedEntries[len(storedEntries)-1])
    textEntries.writelines("]}")
    textEntries.close()

def ReadFile(DB_FILE):
    '''Returns the data from the passed file'''
    with open(DB_FILE, 'r') as entriesFile:
        storedEntries = entriesFile.read()
    entriesFile.close()
    return storedEntries

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
    shuffle(scraped_images)
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
    # 1. Read in stored Missed Connections
    storedEntries = ReadFile(DB_FILE)

    # 2. Load stored Missed Connections as json, if no previous entries
    #   are found create empty lists
    if (len(storedEntries) > 2):
        Entries = json.loads(storedEntries)
        Entries = Entries['posts']
        storedEntries = json.loads(storedEntries)
        storedEntries = storedEntries['posts']
    else:
        storedEntries = []
        Entries = []

    newEntries = []    # A list that stores the posts created from this call

    # 3. Collect hashes of stored Missed Connections
    hashes = CollectEntriesHashes(Entries)

    # 4. Pick a random location, scrape recent posts and chose one to add
    for x in range(0, NUMBER_OF_POSTS):

        # 5. Pick a location randomly
        randomLocationUrl = random.randint(0,2)

        # 6. Collect regional Missed Connections posts linkToVisit
        craigslistMissedConnectionsUrls = CollectMissedConnectionsLink(randomLocationUrl)

        # 7. Shuffle the collected links to randomize selection
        shuffle(craigslistMissedConnectionsUrls)

        # 8. Get Missed Connections post body from the new links
        craigslistMissedConnectionsUrls = CollectMissedConnectionsLink(randomLocationUrl)

        # 9. Get a random number and use it to select the post to be added
        randomPostUrl = random.randint(0,len(craigslistMissedConnectionsUrls)-1)
        finalUrl = craigslistMissedConnectionsUrls[randomPostUrl]

        # 10. Collect the postBody from the selected post
        postBody = GetBody(finalUrl)

        # 11. Hash the post body just gathered
        hashedPostBody = GetHash(postBody)

        # 12. Check if it's already in the store, if not add it and scrape any images found in it
        hashExists = HashExists(hashedPostBody, hashes)
        if (hashExists == 1):
            pageContent = GetPageContent(finalUrl)
            dbEntry = CreateEntry(pageContent, finalUrl, randomLocationUrl)
            print finalUrl
            print dbEntry
            ScrapeImages(finalUrl)
            newEntries.append(str(dbEntry))


    # 13. Write all entries in the store to the db file
    uberEntries = [] # We've opened the file to write so we first must read in all old posts or they'll be lost
    for entry in storedEntries:
        entry = json.dumps(entry)
        uberEntries.append(entry)
    uberEntries = uberEntries + newEntries # Append the new entries to the old
    WriteStoreToFile(('static/data/db.json'), uberEntries)
    directory = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
    if not os.path.isdir("static/data/%s" % directory):
        os.makedirs("static/data/%s" % directory)
    WriteStoreToFile(('static/data/%s/%s.json' % (directory, datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))), newEntries)

    subprocess.call('static/bash/gif_script.sh')
    subprocess.call('static/bash/commit.sh')
    return

count = 0
while True:
    main()
    count = count + 1
    subprocess.call('static/bash/alert.sh')
    sleep = random.randint(1,43200)
    print("\n\n Done for %s seconds, count: %s" % (sleep, count))
    time.sleep(sleep)
