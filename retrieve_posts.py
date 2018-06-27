import psycopg2

def scrape():
    DATABASE_URL='postgres://pkszoedlaykwsk:2ff4fae6161d29c22cf40f349faaa1e48d8524aab1caf6eed72f773a31f0a91b@ec2-54-83-0-158.compute-1.amazonaws.com:5432/d42mu98rpmdqbj'
    conn = psycopg2.connect(DATABASE_URL, sslmode='require', user='pkszoedlaykwsk', password='2ff4fae6161d29c22cf40f349faaa1e48d8524aab1caf6eed72f773a31f0a91b' )
    cur = conn.cursor()
    json_object = {"posts":[]}
    cur.execute( "SELECT title, body, time, location, hash FROM posts_scraped" )
    for title, body, time, location, hash in cur.fetchall() :
        post = {"title": title, "body": body, "time": time, "location": location, "hash": hash}
        json_object['posts'].append(post)

    t = json_object['posts']
    del t[0]
    return json_object
