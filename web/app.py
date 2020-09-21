from flask import Flask
from flask import request
import requests
from retrieve_posts import retrieve_posts
from flask import jsonify
from dateutil import parser
import operator
import os


app = Flask(__name__, static_url_path='')
app.config['DATABASE_URI'] = 'postgres://%s:%s@%s:%s/%s' % (os.environ.get('POSTGRES_USER'), os.environ.get('POSTGRES_PASSWORD'), os.environ.get('POSTGRES_HOST'), os.environ.get('POSTGRES_PORT'), os.environ.get('POSTGRES_DB'))

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
    app.run(host='0.0.0.0')
