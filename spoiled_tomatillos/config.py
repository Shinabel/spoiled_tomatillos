import os

class Config(object):
    """ Default configurations
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    #For authentication
    SECURITY_PASSWORD_SALT = 'yOu_wiLl-NeVEr_GuEsS!@#$'
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    # gmail authentication
    MAIL_USERNAME = os.environ['APP_MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']

    # mail accounts
    MAIL_DEFAULT_SENDER = 'from@example.com'

    # Database information
    SQLALCHEMY_DATABASE_URI = "mysql://spoiled_app:team53letsgo@cs4500-spring2018-morgan.clvsn19ktapw.us-east-2.rds.amazonaws.com:3306/spoiled_tomatillos"
    # allow sql alchemy to track changes to the databse
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class dev_configs(object):
    """ Development configurations
    """
    pass

class test_config(object):
    """ Test configurations
    """
    TEST_STATUS = True
