#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import g
import os
import functions
from time import gmtime, strftime

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


@app.route(path, methods=['GET', 'POST'])
def task():
    args = request.get_json(silent=True)
    print(args)
    if len(args) == 0:
        args = request.form.to_dict()
        if len(args) == 0:
            args = request.args.to_dict()
            if len(args) == 0:
                return "No arguments in request"
    if len(args) > 1:
        return "Got more then 1 argument"
    number = list(args.values())[0]

    if functions.is_number(number) == False:
        return "The argument does not match the task conditions"
    else:
        number = int(number)
    
    values = [i["Number"] for i in list(db.Numbers.find({"Number": { "$in": [number, number+1] } }))]

    if len(values) > 0:
        log = strftime("%d.%m.%Y %H:%M:%S", gmtime()) + " " + str(number) + " Number has already been received\n"
        print(log)
        return "Number has already been received"
    
    values.append(number)
    db.Numbers.insert_one({"Number" : number})
    return str(number + 1)

@app.errorhandler(404)
def not_found(error):
    return "API not found, only " + path + " is available"

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=port)