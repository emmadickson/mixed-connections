from flask import Flask
from flask import request
import requests
from retrieve_posts import retrieve_posts
from flask import jsonify
from dateutil import parser
import operator


app = Flask(__name__, static_url_path='')
app.config['DATABASE_URI']='postgres://jadwwyuaguvfhk:5db0b71a464acaab2ee269c222cbcfeed1e9f9ccd705c22988241ce9575ebc2c@ec2-54-235-108-217.compute-1.amazonaws.com:5432/d5h0m2ld7t3loi?sslmode=require'


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
