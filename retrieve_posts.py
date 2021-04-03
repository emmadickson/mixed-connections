import psycopg2

def retrieve_posts():
    '''Retrieves posts from db so that users can view them'''
    DATABASE_URL='postgres://jadwwyuaguvfhk:5db0b71a464acaab2ee269c222cbcfeed1e9f9ccd705c22988241ce9575ebc2c@ec2-54-235-108-217.compute-1.amazonaws.com:5432/d5h0m2ld7t3loi?sslmode=require'
    conn = psycopg2.connect(DATABASE_URL, sslmode='require', user='jadwwyuaguvfhk', password='5db0b71a464acaab2ee269c222cbcfeed1e9f9ccd705c22988241ce9575ebc2c' )
    cur = conn.cursor()
    json_object = {"posts":[]}
    cur.execute( "SELECT title, body, time, location, hash FROM posts_scraped" )
    for title, body, time, location, hash in cur.fetchall() :
        post = {"title": title, "body": body, "time": time, "location": location, "hash": hash}
        json_object['posts'].append(post)

    t = json_object['posts']
    del t[0]
    return json_object