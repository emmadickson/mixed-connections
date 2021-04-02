import psycopg2

def retrieve_posts():
    '''Retrieves posts from db so that users can view them'''
    DATABASE_URL='postgres://lymvmwhtzfwild:fa8fc31e36f104f9186b3b9fa510e12a0fa6c2c5a096cea30a3573ec8c722341@ec2-54-235-108-217.compute-1.amazonaws.com:5432/d24c2ee90prajs'
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