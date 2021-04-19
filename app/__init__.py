import os
from enum import Enum
from json import dumps, loads

from flask import Flask, render_template, request
from marshmallow import Schema, fields, ValidationError
from marshmallow_enum import EnumField

from .irsystem.models.search import *
app = Flask(__name__, static_folder='../frontend/build/static', template_folder="../frontend/build")

class InputType(Enum):
    text = 1
    code = 2
    both = 3

class SearchFunction(Enum):
    jaccard = 1
    cosine = 2

class SearchSchema(Schema):
    function = EnumField(SearchFunction)
    input_type = EnumField(InputType)
    query = fields.String()
    query_code = fields.String()

@app.route("/")
def index():
    return render_template("index.html")

def df_to_list(df):
    res = []
    for _, row in df.iterrows():
        res.append({
            "url": f'https://stackoverflow.com/questions/{row["q_id"]}',
            "title": row["q_title"]
        })
    return res

@app.route('/search', methods=['POST'])
def search():
    json = request.json
    print(json)
    # Get Request body from JSON
    request_data = request.json
    schema = SearchSchema()
    try:
        # Validate request body against schema data types
        result = schema.load(request_data)
    except ValidationError as err:
        # Return a nice message if validation fails
        return dumps(err.messages), 400

    query, query_code = None, None
    if request_data["input_type"] == "text":
        query = request_data["query"] if len(request_data["query"]) > 0 else None
    elif request_data["input_type"] == "code":
        query_code = request_data["query_code"] if len(request_data["query_code"]) > 0 else None
    else:
        query = request_data["query"] if len(request_data["query"]) > 0 else None
        query_code = request_data["query_code"] if len(request_data["query_code"]) > 0 else None

    res = []
    if request_data["function"] == "cosine":
        res = cosine_combined_search(query, query_code=query_code)
    elif request_data["function"] == "jaccard":
        res = jaccard_search(request_data["query"])

    ret = df_to_list(res)
    return dumps({
        "count": len(ret), "result": ret
    }), 200
