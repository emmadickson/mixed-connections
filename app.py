from flask import Flask
from flask import request
import requests
from retrieve_posts import scrape
from flask import jsonify
from operator import itemgetter


app = Flask(__name__, static_url_path='')
app.config['DATABASE_URI'] = 'postgres://pkszoedlaykwsk:2ff4fae6161d29c22cf40f349faaa1e48d8524aab1caf6eed72f773a31f0a91b@ec2-54-83-0-158.compute-1.amazonaws.com:5432/d42mu98rpmdqbj'

@app.route('/missed')
def render_missed():
    return app.send_static_file('html/missed.html')

@app.route('/')
def render_index():
    return app.send_static_file('html/index.html')

@app.route('/raw_db')
def render_db():
    json_object = scrape()
    posts = json_object['posts']
    json_object['posts'] = sorted(posts,  key=itemgetter('time'), reverse=True)
    return jsonify(json_object)

if __name__ == '__main__':
    app.run()
