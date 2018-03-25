from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_mail import Mail
from flask_login import LoginManager
from werkzeug.utils import find_modules, import_string

pymysql.install_as_MySQLdb()

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)

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

def create_app(config=None):
    """ Factory method creating app
    """
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(Config)

    register_blueprints(app)
    register_cli(app)
    register_teardowns(app)

    return app

def register_blueprints(app):
    """ Registers blueprint modules
    """
    for name in find_modules('app.blueprints'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)
    return None

def register_cli(app):
    """ Registers all cli commands
    """
    @app.cli.command('initdb')
    def initdb_command():
        """ Initializes database connection
        """
        db = SQLAlchemy(app)

def register_teardowns(app):
    """ Teardown methods for when application terminates
    """
    @app.teardown_appcontext
    def close_db(error):
        pass
