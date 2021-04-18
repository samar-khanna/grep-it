import os
from json import dumps, loads

from flask import Flask, render_template, request
from marshmallow import Schema, fields, ValidationError
from marshmallow_enum import EnumField

from .irsystem.models.search import *
app = Flask(__name__, static_folder='../frontend/build/static', template_folder="../frontend/build")

@app.route("/")
def index():
    return render_template("index.html")

class InputType(Enum):
    text = 1
    code = 2

class SearchFunction(Enum):
    jaccard = 1
    cosine = 2

class SearchSchema(Schema):
    function = EnumField(SearchFunction)
    input_type = EnumField(InputType)
    query = fields.String(required=True)


@app.route('/')
def hello():
    return 'Hello, World!'


# controller for now
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('search')
    if not query:
        results = []
        query_confirmation = ''
    else:
        query_confirmation = "Your search: " + query
        results = jaccard_search(query)  # top results from search.py
    return render_template('index.html', query_confirmation=query_confirmation, results=results)

def df_to_list(df):
    res = []
    for _, row in df.iterrows():
        res.append({
            "url": f'https://stackoverflow.com/questions/{row["q_id"]}'
        })
    return res

@app.route('/search', methods=['GET'])
def search():
    json = request.json
    # Get Request body from JSON
    request_data = request.json
    schema = SearchSchema()
    try:
        # Validate request body against schema data types
        result = schema.load(request_data)
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify(err.messages), 400

    search_req_json = dumps(result)

    if search_req_json["function"] is "cosine":
        res = cosine_combined_search(query)
    elif search_req_json["function"] is "jaccard":
        res = jaccard_search(query)

    ret = df_to_list(res)
    return json.dumps({
        "count": len(ret), "result": ret
    }), 200
