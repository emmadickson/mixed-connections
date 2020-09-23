import psycopg2
import os
import csv

def retrieve_random_post():
    '''Retrieves random post from db'''
    DATABASE_URL = 'postgres://%s:%s@%s:%s/%s' % (os.environ.get('POSTGRES_USER'), os.environ.get('POSTGRES_PASSWORD'), os.environ.get('POSTGRES_HOST'), os.environ.get('POSTGRES_PORT'), os.environ.get('POSTGRES_DB'))

    conn = psycopg2.connect(DATABASE_URL, user='postgres', password='postgres' )
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
    DATABASE_URL = 'postgres://%s:%s@%s:%s/%s' % (os.environ.get('POSTGRES_USER'), os.environ.get('POSTGRES_PASSWORD'), os.environ.get('POSTGRES_HOST'), os.environ.get('POSTGRES_PORT'), os.environ.get('POSTGRES_DB'))
    conn = psycopg2.connect(DATABASE_URL, user='postgres', password='postgres')
    cur = conn.cursor()
    json_object = {"posts":[]}
    cur.execute( "SELECT body,time,hash,location,title FROM posts_scraped" )
    for body,time,hash,location,title in cur.fetchall() :
        post = {"body": body, "time": time, "hash": hash, "location": location, "title": title}
        json_object['posts'].append(post)
    
    t = json_object['posts']
    return json_object
    
def retrieve_posts_csv():
    '''Retrieves posts from db as csv so users can seed their own db'''
    DATABASE_URL = 'postgres://%s:%s@%s:%s/%s' % (os.environ.get('POSTGRES_USER'), os.environ.get('POSTGRES_PASSWORD'), os.environ.get('POSTGRES_HOST'), os.environ.get('POSTGRES_PORT'), os.environ.get('POSTGRES_DB'))

    conn = psycopg2.connect(DATABASE_URL, user='postgres', password='postgres' )
    cur = conn.cursor()
    posts = "body,time,hash,location,title\n"
    cur.execute( "SELECT body,time,hash,location,title FROM posts_scraped" )
    for body,time,hash,location,title in cur.fetchall() :
        post = '"%s",%s,%s,%s,"%s"\n' % (body,time,hash,location,title)
        posts = posts + post   
    return posts
        
    