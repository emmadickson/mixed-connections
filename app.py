from flask import Flask
from flask import request
import requests
from retrieve_posts import retrieve_posts
from flask import jsonify
from dateutil import parser
import operator


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
    json_object = retrieve_posts()
    return jsonify(json_object)

@app.route('/pretty_db')
def render_pretty_db():
    json_object = retrieve_posts()
    posts = json_object['posts']
    for post in posts:
        date = post['time']
        d = parser.parse(date)
        post['time'] = d.strftime("%Y-%m-%d")

    json_object['posts'].sort(key=operator.itemgetter('time'), reverse=True)
    return jsonify(json_object)

if __name__ == '__main__':
    app.run()
