import pycassa
import bisect
import hashlib
import sys
import json
import bigcorrect

from pycassa.system_manager import *
from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily
from flask import Flask
from flask import url_for
from flask import request
from flask import render_template
from pprint import  pprint
from flask import make_response

app = Flask(__name__)
select=[]
clusters=[]
centers=[]
xs=[]
vocab={}
@app.route('/')
def home1():
	return render_template('home.html')

@app.route('/home')
def home():
  return render_template('home.html')

@app.route('/insert', methods=['GET', 'POST'])
def insert():
	if request.method == 'POST':
		# Invoking Method insertTweets
		file_path = request.form["filePath"]
		print file_path
		bigcorrect.func(file_path)
		return render_template('insertRes.html')
	return render_template('insert.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
	if request.method == 'POST':
		# Invoking Method searchTweets
		tweet_words = request.form["tweetWords"]
		print tweet_words
		resp = bigcorrect.funcmain(tweet_words)
		#respDict = json.loads(resp)
		respDict = resp
		print respDict
		return render_template('searchRes.html', respDict=respDict)
  	return render_template('search.html')

@app.route('/contactUs')
def contactUs():
	return render_template('contactUs.html')

if __name__ == '__main__':
       app.run(debug=True)
