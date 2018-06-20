from flask import Flask
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

app = Flask(__name__, static_url_path='')

# Constants
CRAIGSLIST_URLS = [
"https://newyork.craigslist.org",
"https://raleigh.craigslist.org",
"https://pittsburgh.craigslist.org"
]

NUMBER_OF_POSTS = 10
DB_FILE = "static/data/db.json"
ENTRIES_FILE = "static/data/entries.json"


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
    print("Post from " + location + " added")
    dbEntry = "{ \"title\": " + "\"" + title + "\"" +  ", \"body\": " \
    + "\"" + body + "\"" + ", \"location\": " + "\"" + location + "\"" + \
    ", \"time\": " + "\"" + str(today) + "\"" + ", \"hash\": " + "\"" + \
    str(hashedPostBody) + "\"" "}"
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
    '''Scrapes all the images found in a post from the url passed'''
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
    image_number = len(scraped_images)
    images = set(images)
    for img in images:
        if ("50x50" not in img) and img not in IMAGE_HASHES:
            file = cStringIO.StringIO(urllib2.urlopen(img).read())
            img = Image.open(file)
            image_number = image_number + 1
            img.save("static/images/scraped_images/" + str(image_number) + ".jpg", "JPEG")
            print "image saved!"

@app.route('/missed')
def render_missed():
    return app.send_static_file('html/missed.html')

@app.route('/')
def render_index():
    return app.send_static_file('html/index.html')

@app.route('/raw_db')
def render_db():
    return app.send_static_file('data/db.json')

if __name__ == '__main__':
    app.run()
