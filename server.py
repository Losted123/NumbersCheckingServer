from flask import Flask
from flask import request
from flask import g
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import functions
from time import gmtime, strftime

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Numbers.sqlite3'
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)
class Number(db.Model):
    __tablename__ = 'NUMBERS'
    __table_args__ = { 'extend_existing': True }
    Number = db.Column(db.Integer, unique=True, nullable=False)

values = [i[0] for i in db.session.query(Number.Number).all()]

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
    
    if number in values or (number + 1) in values:
        log = strftime("%d.%m.%Y %H:%M:%S", gmtime()) + " " + str(number) + " Number has already been received\n"
        f = open("log.txt", "a")
        f.write(log)
        f.close()
        return "Number has already been received"
    
    values.append(number)
    db.session.add(Number(Number=number))
    db.session.commit()
    return str(number + 1)

@app.errorhandler(404)
def not_found(error):
    return "API not found, only " + path + " is available"

if __name__ == "__main__":
    app.run(port=port)