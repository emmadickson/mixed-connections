from flask import Flask
import requests
import socks
import socket
import bs4
import hashlib
import re
import datetime
from random import shuffle
import random
app = Flask(__name__, static_url_path='')

# Constants
CRAIGSLIST_URLS = [
"https://newyork.craigslist.org",
"https://raleigh.craigslist.org",
"https://pittsburgh.craigslist.org"
]
NUMBER_OF_POSTS = 2
DB_FILE = "static/db.txt"

randomUrl = random.randint(0,2)

def CollectEntriesHashes(storedEntries):
    hashes = []
    for entry in storedEntries:
        entryFields = entry.split("***")
        if len(entryFields) > 3:
            hash = entryFields[2]
            hash = hash[1:]
            hashes.append(hash)
    return hashes

def CollectMissedConnectionsLink():
    craigslistMissedConnectionsUrls = []
    randomCraigslistUrl = CRAIGSLIST_URLS[randomUrl] + "/search/mis"
    response = requests.get(randomCraigslistUrl).text
    soup = bs4.BeautifulSoup(response, "html.parser")
    for link in soup.findAll('a', href=True, text=''):
            if ('html' in link['href']):
                craigslistMissedConnectionsUrls.append( link['href'] )
    shuffle(craigslistMissedConnectionsUrls)
    return craigslistMissedConnectionsUrls

def GetTitle(pageContent):
    title = pageContent.select('title')[0].get_text()
    title = CleanTitle(title)
    return title

def GetLocation():
    location = CRAIGSLIST_URLS[randomUrl]
    if ".org" in location:
        location = CRAIGSLIST_URLS[randomUrl][8:-15]
    else:
        location = CRAIGSLIST_URLS[randomUrl][8:-14]
    return location

def GetHash(postBody):
    hashObject = hashlib.md5(postBody)
    hashedPostBody = hashObject.hexdigest()
    return hashedPostBody;

def GetPageContent(craigslistMissedConnectionsUrls):
    linkToVisit = craigslistMissedConnectionsUrls[0]
    response = requests.get(linkToVisit)
    pageContent = bs4.BeautifulSoup(response.text, "html.parser")
    return pageContent;

def GetBody():
    craigslistMissedConnectionsUrls = CollectMissedConnectionsLink()
    pageContent = GetPageContent(craigslistMissedConnectionsUrls)
    body = pageContent.select('section#postingbody')[0].get_text()
    body = body.split("QR Code Link to This Post")[1]
    body = CleanPostBody(body)
    return body

def CleanPostBody(body):
    body = re.sub('\n', '', body)
    body = (body).replace('"', "'")
    body = body.rstrip()
    body = body.encode('utf-8')
    return body

def CleanTitle(title):
    title = re.sub('\n', '', title)
    title = (title).replace('"', "'")
    title = title.encode('utf-8')
    return title

def CleanStoredEntries(storedEntries):
    storedEntries = storedEntries[16:]
    storedEntries = storedEntries[:-5]
    storedEntries = storedEntries.split("\",\"")
    return storedEntries

def CheckIfHashExists(hashedPostBody, hashes):
    if (hashedPostBody not in hashes):
        return True
    else:
        return False

def CreateEntry(pageContent):
    title = GetTitle(pageContent)
    today = datetime.date.today()
    location = GetLocation()
    body = GetBody()
    hashedPostBody = GetHash(body)
    dbEntry = title + " *** " + body + " *** " + hashedPostBody + "*** Location: " + location + " *** Time: " + str(today)
    return dbEntry

def AddEntryToStore(storedEntries, pageContent):
    dbEntry = CreateEntry(pageContent)
    print(dbEntry)
    storedEntries.append(dbEntry)
    return storedEntries

def WriteStoreToFile(storedEntries):
    textEntries = open('static/db.txt', 'w')
    textEntries.write("var entries = [")
    for line in storedEntries:
        if (line != None and len(line) > 2):
            textEntries.write("\"" + line + "\",")
            textEntries.write(" ")
    textEntries.write("];")
    textEntries.close()

def ReadFile(DB_FILE):
    with open(DB_FILE, 'r') as entriesFile:
        storedEntries = entriesFile.read()
    entriesFile.close()
    return storedEntries

@app.route('/')
def render_index():
    return app.send_static_file('html/index.html')

@app.route('/db')
def render_db():
    return app.send_static_file('html/db.html')

@app.route('/raw_db')
def render_raw_db():
    return app.send_static_file('db.txt')

@app.route('/fibs')
def render_fibs():
    return app.send_static_file('html/fibs/fib.html')

@app.route('/frame_8.1')
def render_8_1():
    return app.send_static_file('html/fibs/frame8.1.html')

@app.route("/bots")
def webscrape():
    craigslistMissedConnectionsUrls = CollectMissedConnectionsLink()

    storedEntries = ReadFile(DB_FILE)

    storedEntries = CleanStoredEntries(storedEntries)

    hashes = CollectEntriesHashes(storedEntries)

    for x in range(0, NUMBER_OF_POSTS):
        postBody = GetBody()

        hashedPostBody = GetHash(postBody)

        hashExists = CheckIfHashExists(hashedPostBody, hashes)

        if (hashExists == 1):
            pageContent = GetPageContent(craigslistMissedConnectionsUrls)
            storedEntries = AddEntryToStore(storedEntries, pageContent)

    WriteStoreToFile(storedEntries)

    return app.send_static_file('html/bots.html')


if __name__ == '__main__':
    app.run()
