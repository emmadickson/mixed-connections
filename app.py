from flask import Flask
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
app = Flask(__name__, static_url_path='')

# Constants
CRAIGSLIST_URLS = [
"https://newyork.craigslist.org",
"https://raleigh.craigslist.org",
"https://pittsburgh.craigslist.org"
]
NUMBER_OF_POSTS = 5
DB_FILE = "static/db.json"


def CollectEntriesHashes(storedEntries):
    hashes = []
    for entry in storedEntries:
        hash = entry['hash']
        hashes.append(hash)
    return hashes

def CollectMissedConnectionsLink(randomLocationUrl):
    craigslistMissedConnectionsUrls = []
    randomCraigslistUrl = CRAIGSLIST_URLS[randomLocationUrl] + "/search/mis"
    response = requests.get(randomCraigslistUrl).text
    soup = bs4.BeautifulSoup(response, "html.parser")
    for link in soup.findAll('a', href=True, text=''):
            if ('html' in link['href']):
                craigslistMissedConnectionsUrls.append( link['href'] )
    return craigslistMissedConnectionsUrls

def GetTitle(pageContent):
    title = pageContent.select('title')[0].get_text()
    title = CleanTitle(title)
    return title

def GetLocation(randomLocationUrl):
    location = CRAIGSLIST_URLS[randomLocationUrl]
    if ".org" in location:
        location = CRAIGSLIST_URLS[randomLocationUrl][8:-15]
    else:
        location = CRAIGSLIST_URLS[randomLocationUrl][8:-14]
    return location

def GetHash(postBody):
    hashObject = hashlib.md5(postBody)
    hashedPostBody = hashObject.hexdigest()
    return hashedPostBody;

def GetPageContent(linkToVisit):
    response = requests.get(linkToVisit)
    pageContent = bs4.BeautifulSoup(response.text, "html.parser")
    return pageContent;

def GetBody(randomPostUrl, randomLocationUrl):
    craigslistMissedConnectionsUrls = CollectMissedConnectionsLink(randomLocationUrl)
    pageContent = GetPageContent(craigslistMissedConnectionsUrls[randomPostUrl])
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

def HashExists(hashedPostBody, hashes):
    if (hashedPostBody not in hashes):
        return True
    else:
        return False

def CreateEntry(pageContent, randomPostUrl, randomLocationUrl):
    title = GetTitle(pageContent)
    today = datetime.date.today()
    location = GetLocation(randomLocationUrl)
    body = GetBody(randomPostUrl, randomLocationUrl)
    hashedPostBody = GetHash(body)
    print("Post from " + location + " added")
    dbEntry = "{ \"title\": " + "\"" + title + "\"" +  ", \"body\": " \
    + "\"" + body + "\"" + ", \"location\": " + "\"" + location + "\"" + \
    ", \"time\": " + "\"" + str(today) + "\"" + ", \"hash\": " + "\"" + \
    str(hashedPostBody) + "\"" "}"
    return dbEntry

def WriteStoreToFile(storedEntries):
    textEntries = open('static/db.json', 'w')
    textEntries.write("{\"posts\":[")
    for x in range(0, len(storedEntries)-2):
        if (storedEntries[x] != None and len(storedEntries[x]) > 2):
            textEntries.write(str(storedEntries[x]))
            textEntries.write(",")
    textEntries.write(storedEntries[len(storedEntries)-1])
    textEntries.writelines("]}")
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
    return app.send_static_file('db.json')

@app.route('/raw_thesaurus')
def render_raw_thesaurus():
    return app.send_static_file('ea-thesaurus.json')

@app.route('/add/<string:post>')
def user(post):
    print('WELL HALLO IN THAR')
    print(post)
    return app.send_static_file('html/feed.html')

@app.route('/raw_dict')
def render_raw_dict():
    return app.send_static_file('dictionary.json')

@app.route('/feed')
def render_fibs():
    return app.send_static_file('html/feed.html')

@app.route("/bots")
def webscrape():
    # 1. Read in stored Missed Connections
    storedEntries = ReadFile(DB_FILE)

    # 2. Clean stored Missed Connections
    if (len(storedEntries) > 2):
        Entries = json.loads(storedEntries)
        Entries = Entries['posts']
        storedEntries = json.loads(storedEntries)
        storedEntries = storedEntries['posts']
    else:
        storedEntries = []
        Entries = []

    newEntries = []
    # 3. Collect hashes of stored Missed Connections
    hashes = CollectEntriesHashes(Entries)
    print(hashes)

    for x in range(0, NUMBER_OF_POSTS):
        # 4. Pick a location randomly
        randomLocationUrl = random.randint(0,2)
        # 4. Collect Missed Connections Post Link
        craigslistMissedConnectionsUrls = CollectMissedConnectionsLink(randomLocationUrl)
        # 5. Shuffle the collected links to randomize selection
        shuffle(craigslistMissedConnectionsUrls)
        # 6. Get a random number
        randomPostUrl = random.randint(0,len(craigslistMissedConnectionsUrls)-1)
        # 7. Get Missed Connections post body from the new links
        postBody = GetBody(randomPostUrl, randomLocationUrl)
        # 7. Hash the post body just gathered
        hashedPostBody = GetHash(postBody)
        # 8. Check if it's already in the store, if not add it
        hashExists = HashExists(hashedPostBody, hashes)
        if (hashExists == 1):
            linkToVisit = craigslistMissedConnectionsUrls[randomPostUrl]
            pageContent = GetPageContent(linkToVisit)
            dbEntry = CreateEntry(pageContent, randomPostUrl, randomLocationUrl)
            newEntries.append(str(dbEntry))

    # 9. Write all entries in the store to the db file
    uberEntries = []
    storedEntries
    for entry in storedEntries:
        entry = json.dumps(entry)
        uberEntries.append(entry)

    uberEntries = uberEntries + newEntries
    WriteStoreToFile(uberEntries)

    return app.send_static_file('html/bots.html')


if __name__ == '__main__':
    app.run()
