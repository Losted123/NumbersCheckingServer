#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import g
import os
import functions
from time import gmtime, strftime
from flask import jsonify

import pymongo
from pymongo import MongoClient

app = Flask(__name__)

# Enviroment init
path = os.environ.get('API_PATH')
port = os.environ.get('API_PORT')
db_path = os.environ.get("DB_PATH")
db_port = os.environ.get("DB_PORT")
if path is None or port is None or db_path is None or db_port is None:
    raise Exception('Add API_PATH, API_PORT, DB_PATH and DB_PORT env vars')

# Database init
client = MongoClient("mongodb://" + db_path + ":" + db_port)
db = client.Numbers

try:
    db.Numbers.create_index("Number", unique=True )
except pymongo.errors.DuplicateKeyError as e:
    print("\ncreate index error: " + str(e.details))


@app.route(path, methods=['GET', 'POST'])
def task():
    args = request.get_json(silent=True)
    print(args)
    if args is None:
        args = request.form.to_dict()
        if len(args) == 0:
            args = request.args.to_dict()
            if len(args) == 0:
                return jsonify({"error": "No arguments in request"})
    if len(args) > 1:
        return jsonify({"error":"Got more then 1 argument"})
    number = list(args.values())[0]

    if functions.is_number(number) == False:
        return jsonify({"error":"The argument does not match the task conditions"})
    else:
        number = int(number)
    
    try:
        db.Numbers.insert_many([
            {"Number" : number},
            {"Number" : number-1}
        ], ordered=True)
    except pymongo.errors.DuplicateKeyError as e:
        print("\ncreate index error: " + str(e.details))
    except pymongo.errors.BulkWriteError as e:
        print("\nBULKerror: " + str(e.details))
        if e.details["writeErrors"][0]["keyValue"]["Number"] != number - 1:
            log = strftime("%d.%m.%Y %H:%M:%S", gmtime()) + " " + str(number) + " Number has already been received\n"
            print(log)
            return jsonify({"error":"Number '" + str(number) + "' has already been received"})
    
    return jsonify({"response": str(number + 1)})

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error":"API not found, only " + path + " is available"})

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=port)