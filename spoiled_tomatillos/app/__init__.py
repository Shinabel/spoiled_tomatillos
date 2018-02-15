from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# connecting to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://spoiled_app:team53letsgo@cs4500-spring2018-morgan.clvsn19ktapw.us-east-2.rds.amazonaws.com:3306/spoiled_tomatillos'
# allow sql alchemy to track changes to the databse
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['DEBUG']=True
# creating the database object
db = SQLAlchemy(app)
from app import routes
