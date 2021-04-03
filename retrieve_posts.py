import psycopg2

def retrieve_posts():
    '''Retrieves posts from db so that users can view them'''
    DATABASE_URL=os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require', user=os.environ['DATABASE_USER'], password=os.environ['DATABASE_PASSWORD'])
    cur = conn.cursor()
    json_object = {"posts":[]}
    cur.execute( "SELECT title, body, time, location, hash FROM posts_scraped" )
    for title, body, time, location, hash in cur.fetchall() :
        post = {"title": title, "body": body, "time": time, "location": location, "hash": hash}
        json_object['posts'].append(post)

    t = json_object['posts']
    del t[0]
    return json_object