from flask import Flask
from flask import request
from flask import g
import os
from dotenv import load_dotenv
import functions
from time import gmtime, strftime

from pymongo import MongoClient

app = Flask(__name__)

# Enviroment init
dotenv_path = os.path.join(os.path.dirname(__file__), 'settings.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    path = os.getenv('path')
    port = os.getenv('PORT')
else:
    raise Exception('settings.env not found')

# Database init
client = MongoClient('localhost:27017')
db = client.Numbers


@app.route(path, methods=['GET', 'POST'])
def task():
    args = request.form.to_dict()
    if len(args) == 0:
        args = request.args.to_dict()
        if len(args) == 0:
            return "No arguments in request"
    if len(args) > 1:
        return "Got more then 1 argument"
    number = list(args.values())[0]
    print(args)

    if functions.is_number(number) == False:
        return "The argument does not match the task conditions"
    else:
        number = int(number)
    
    values = [i["Number"] for i in list(db.Numbers.find())]
    if number in values or (number + 1) in values:
        log = strftime("%d.%m.%Y %H:%M:%S", gmtime()) + " " + str(number) + " Number has already been received\n"
        f = open("log.txt", "a")
        f.write(log)
        f.close()
        return "Number has already been received"
    
    values.append(number)
    db.Numbers.insert_one({"Number" : number})
    return str(number + 1)

@app.errorhandler(404)
def not_found(error):
    return "API not found, only " + path + " is available"

if __name__ == "__main__":
    app.run(port=port)