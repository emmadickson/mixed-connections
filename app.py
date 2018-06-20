from flask import Flask
from flask import request
import requests
import socks
import socket
import bs4
import hashlib
import re
import json
import datetime
from random import shuffle
import random
import os
from PIL import Image
import urllib2
import cStringIO
import subprocess

app = Flask(__name__, static_url_path='')

@app.route('/missed')
def render_missed():
    return app.send_static_file('html/missed.html')

@app.route('/')
def render_index():
    return app.send_static_file('html/index.html')

@app.route('/raw_db')
def render_db():
    return app.send_static_file('data/db.json')

<<<<<<< HEAD
=======

>>>>>>> 036f963502caec767bc1a58c16dded07778d64a5
if __name__ == '__main__':
    app.run()
