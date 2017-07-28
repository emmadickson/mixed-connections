from flask import Flask
import requests
import socks
import socket
import bs4
import hashlib
import re
import datetime
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy

app = Flask(__name__)

@app.route("/")
def webscrape():
    # 1. Specify the local url
    baseURL = "https://newyork.craigslist.org"
    startURL = baseURL + "/search/mis"

    socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9050)
    socket.socket = socks.socksocket
    # 2. Get the links on the missed connections page provided
    response = requests.get(startURL).text
    print response
    soup = bs4.BeautifulSoup(response, "html.parser")
    links = soup.select('p.result-info a[href^=/]')
    links = [a.attrs.get('href') for a in soup.select('p.result-info a[href^=/]')]

    # 3. Go through the links and add the base url to create final links
    # initially limited to 3
    finalLinks = []
    for x in range(0, 3):
        finalLink = baseURL + links[x]
        finalLinks.append(finalLink)

    # 4. Read in the db info and store hashes of titles also remove last line
    # of js wrapping
    hashes = []
    with open('public/docs/db.txt') as f:
        lines = f.read().splitlines()
    f.close()

    w = open('public/docs/db.txt', 'w')
    w.writelines([item and "\n" for item in lines[:-1]])
    w.close()

    for l in lines:
        hash = l.split("***")
        if len(hash) == 3:
            hashes.append(hash)

    # 5. Scrape the titles and postbody and add to db file

    text_file = open('public/docs/db.txt', "a")

    for finalLink in finalLinks:
        socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9050)
        socket.socket = socks.socksocket
        response = requests.get(finalLink)
        pageContent = bs4.BeautifulSoup(response.text, "html.parser")
        title = pageContent.select('title')[0].get_text()
        # 6. Hash title and check to see if we've already stored it.
        # If not construct db entry and add it to file
        hash_object = hashlib.md5(title)
        titleHash = hash_object.hexdigest()

        if (titleHash not in hashes):
            body = pageContent.select('section#postingbody')[0].get_text()
            body = body.split("QR Code Link to This Post")[1]
            title = re.sub('\n', '', title)
            body = re.sub('\n', '', body)
            body = rstrip()
            dbEntry = "\n" + title + " *** " + body + " *** " + titleHash + " *** " + datetime.date.today() + "\n"

            text_file.write(dbEntry)
    text_file.write("\n")
    text_file.write('`;')
    text_file.close()
    return "Hello World!"
