import os
from flask import Flask, send_from_directory, render_template, request
from .irsystem.models.search import *
app = Flask(__name__, static_folder='../frontend/build/static', template_folder="../frontend/build")

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/search', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
	    results = []
	    query_confirmation = ''
	else:
		query_confirmation = "Your search: " + query
	return {"query": query_confirmation}, 200
