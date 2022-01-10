import requests
import bs4
import hashlib
import re
import datetime
import random
import pandas as pd
import sys

# Constants
CRAIGSLIST_URLS = [
"https://newyork.craigslist.org",
"https://raleigh.craigslist.org",
"https://pittsburgh.craigslist.org",
"https://maine.craigslist.org/"
]

NUMBER_OF_POSTS = int(sys.argv[1])


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
    hashedPost = GetHash(body)
    # For debugging purposes

    print("Post from %s fetched" % location)
    print(body)
    return (title.decode('utf-8'), body.decode('utf-8'), str(location), str(today), str(hashedPost))

def main():
    json_object = []

    #   4. Pick a random location, scrape recent posts and chose one to add
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
        json_object.append({'title': data[0], 'body': data[1], "location": data[2], "time": data[3], "hash":data[4]})

    dataframe = pd.DataFrame.from_records(json_object)
    print(dataframe)
    dataframe.to_csv('output.csv', index=False)
    return


main()

print("Done Scraping")
