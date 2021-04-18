import os
from flask import Flask, render_template, request
from .irsystem.models.search import *
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

#controller for now
@app.route('/search', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
	    results = []
	    query_confirmation = ''
	else:
		query_confirmation = "Your search: " + query
		results = test(query) #top results from search.py
	return render_template('index.html', query_confirmation=query_confirmation, results=results)
