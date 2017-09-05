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
app = Flask(__name__)

@app.route('/')
def render_static():
    return app.send_static_file('index.html')

@app.route('/db')
def render_statics():
    return app.send_static_file('db.html')

@app.route('/raw')
def render_staticd():
    return app.send_static_file('db.txt')

@app.route("/bots")
def webscrape():
    # 1. Specify the local url
    homeBases = ["https://newyork.craigslist.org",
    "https://raleigh.craigslist.org",
    "https://pittsburgh.craigslist.org",
    "https://berlin.craigslist.de"]

    totalPostNumber = 10
    for x in range (0, totalPostNumber):
        randomUrl = random.randint(0,3)
        startURL = homeBases[randomUrl] + "/search/mis"

        #socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9050)
        #socket.socket = socks.socksocket

        # 2. Get the links on the missed connections page provided
        response = requests.get(startURL).text

        soup = bs4.BeautifulSoup(response, "html.parser")
        links = soup.select('p.result-info a[href^=/]')
        links = [a.attrs.get('href') for a in soup.select('p.result-info a[href^=/]')]
        shuffle(links)

        # 3. Go through the links and add the base url to create final links
        finalLinks = []
        finalLink = homeBases[randomUrl] + links[0]
        finalLinks.append(finalLink)

        # 4. Read in the db info and store hashes of titles also remove last line
        # of js wrapping
        hashes = []
        with open('public/docs/db.txt', 'r') as f:
            lines = f.read()
        f.close()

        lines = lines[16:]
        lines = lines[:-5]
        lines = lines.split("\",\"")

        for l in lines:
            hash = l.split("***")
            if len(hash) > 3:
                h = hash[2]
                h = h[1:]
                hashes.append(h)

        # 5. Scrape the titles and postbody and add to db file
        open('public/docs/db.txt', 'w').close()

        text_file = open('public/docs/db.txt', 'w')

        for finalLink in finalLinks:
            #socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9050)
            #socket.socket = socks.socksocket
            response = requests.get(finalLink)
            pageContent = bs4.BeautifulSoup(response.text, "html.parser")
            body = pageContent.select('section#postingbody')[0].get_text()
            body = body.split("QR Code Link to This Post")[1]
            body = re.sub('\n', '', body)
            body = (body).replace('"', "'")
            body = body.rstrip()
            body = body.encode('utf-8')

            # 6. Hash title and check to see if we've already stored it.
            # If not construct db entry and add it to file
            hash_object = hashlib.md5(body)
            bodyHash = hash_object.hexdigest()

            if (bodyHash not in hashes):
                print("Add!")


                title = pageContent.select('title')[0].get_text()
                title = re.sub('\n', '', title)
                title = (title).replace('"', "'")
                title = title.encode('utf-8')
                today = datetime.date.today()
                location = homeBases[randomUrl]
                if ".org" in location:
                    location = homeBases[randomUrl][8:-15]
                else:
                    location = homeBases[randomUrl][8:-14]
                print location
                dbEntry = title + " *** " + body + " *** " + bodyHash + "*** Location: " + location + " *** Time: " + str(today)
                lines.append(dbEntry)

        text_file.write("var entries = [")
        for line in lines:
            if len(line) > 2:
                print(line)
                text_file.write("\"" + line + "\",")
                text_file.write(" ")

        text_file.write("];")
        text_file.close()

    return "Bling bling bitch do my own thing bitch"

if __name__ == '__main__':
    app.run()
