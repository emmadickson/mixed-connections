from flask import Flask, send_file, make_response
from flask import request
import requests
from retrieve_posts import retrieve_posts, retrieve_posts_csv, retrieve_random_post
from flask import jsonify
from dateutil import parser
import operator
import os
import json


app = Flask(__name__, static_url_path='')
app.config['DATABASE_URI'] = os.environ.get('DATABASE_URL')

@app.route('/missed')
def render_missed():
    return app.send_static_file('html/missed.html')

@app.route('/formatted_db')
def render_test():
    return app.send_static_file('html/db_view.html')

@app.route('/')
def render_index():
    return app.send_static_file('html/index.html')

@app.route('/raw_db')
def render_db():
    json_object = retrieve_posts()
    return jsonify(json_object)

@app.route('/random_post')
def render_random_post():
    return retrieve_random_post()

@app.route('/output.csv')
def download_csv():
    csv = retrieve_posts_csv()
    response = make_response(csv)
    cd = 'attachment; filename=output.csv'
    response.headers['Content-Disposition'] = cd
    response.mimetype='text/csv'
    return response

@app.route('/pretty_db')
def render_pretty_db():
    json_object = retrieve_posts()
    posts = json_object['posts']
    for post in posts:
        date = post['time']
        d = parser.parse(date)
        post['time'] = d.strftime("%Y-%m-%d")
    json_object['posts'][0:500].sort(key=operator.itemgetter('time'), reverse=True)
    return jsonify(json_object)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
