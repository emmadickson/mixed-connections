
import psycopg2
import os
import csv

def retrieve_random_post():
    '''Retrieves random post from db'''
    DATABASE_URL =  os.environ.get('DATABASE_URL')

    conn = psycopg2.connect(DATABASE_URL, sslmode='require', user=os.environ.get('DATABASE_USER'), password=os.environ.get('DATABASE_PASSWORD'))
    cur = conn.cursor()
    cur.execute( "SELECT body,time,hash,location,title FROM posts_scraped OFFSET floor(random()*(SELECT count(*) from posts_scraped)) LIMIT 25;" )
    json_object = {"posts":[]}
    for body,time,hash,location,title in cur.fetchall() :
        post = {"body": body, "time": time, "hash": hash, "location": location, "title": title}
        json_object['posts'].append(post)

    t = json_object['posts']
    return json_object

def retrieve_posts():
    '''Retrieves posts from db so that users can view them'''
    DATABASE_URL =  os.environ.get('DATABASE_URL')
    conn = psycopg2.connect(DATABASE_URL, sslmode='require', user=os.environ.get('DATABASE_USER'), password=os.environ.get('DATABASE_PASSWORD'))
    cur = conn.cursor()
    json_object = {"posts":[]}
    cur.execute( "SELECT body,time,hash,location,title FROM posts_scraped ORDER BY time DESC LIMIT 1000" )
    for body,time,hash,location,title in cur.fetchall() :
        post = {"body": body, "time": time, "hash": hash, "location": location, "title": title}
        json_object['posts'].append(post)
    
    t = json_object['posts']
    return json_object
    
def retrieve_posts_csv():
    '''Retrieves posts from db as csv so users can seed their own db'''
    DATABASE_URL =  os.environ.get('DATABASE_URL')

    conn = psycopg2.connect(DATABASE_URL, sslmode='require', user=os.environ.get('DATABASE_USER'), password=os.environ.get('DATABASE_PASSWORD'))
    cur = conn.cursor()
    posts = "body,time,hash,location,title\n"
    cur.execute( "SELECT body,time,hash,location,title FROM posts_scraped" )
    for body,time,hash,location,title in cur.fetchall() :
        post = '"%s",%s,%s,%s,"%s"\n' % (body,time,hash,location,title)
        posts = posts + post   
    return posts