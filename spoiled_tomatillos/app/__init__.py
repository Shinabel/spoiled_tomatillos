from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_mail import Mail
from flask_login import LoginManager

pymysql.install_as_MySQLdb()

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)


# connecting to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://spoiled_app:team53letsgo@cs4500-spring2018-morgan.clvsn19ktapw.us-east-2.rds.amazonaws.com:3306/spoiled_tomatillos'
# allow sql alchemy to track changes to the databse
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['DEBUG']=True
# creating the database object
db = SQLAlchemy(app)

#creating login manager
login_manager = LoginManager()
login_manager.init_app(app)

#creating a mail
mail = Mail(app)

from app.dbobjects import UserInfo

login_manager.login_view = "user.login"
login_manager.login_message_category = "danger"

@login_manager.user_loader
def load_user(user_id):
    return UserInfo.query.filter(UserInfo.user_ID == int(user_id)).first()


from app import routes
