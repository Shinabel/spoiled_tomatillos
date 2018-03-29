import unittest
import os
from config import Config
import pytest
#import ipdb

'''
@pytest.fixture
def app():
    return test_app
'''

@pytest.fixture
def client():
    """ Fixture setting up testing environemtn
    TODO: Add more environment info, sepatate testing config
    """
    from app import app
    app.config.from_object(Config)
    client = app.test_client()
    yield client

def test_app(client):
    pass

# def test_db_object(client):
#     from app import db

def test_login_manager(client):
    from app import login_manager

# def test_create_app(client):
#     from app import create_app
#     create_app()

def test_test_config(client):
    from config import Config
    from config import test_config

def test_dbobjects(client):
    from app import dbobjects

def test_user_info_methods(client):
    from app import dbobjects
    ui = dbobjects.UserInfo
    ui.is_active
    ui.get_id
    ui.is_authenticated
    ui.is_anonymous

def test_email(client):
    from app import email

def test_imports(client):
    import flask
    import flask_sqlalchemy
    import pymysql
    import flask_mail
    import flask_login
    import werkzeug
    import flask_wtf
    import passlib
    import wtforms
    import itsdangerous
    import bs4
    import requests

def test_init_load_user(client):
    try:
        from app import load_user
        load_user(1)
    except:
        pass

def test_index(client):
    client.get('/', follow_redirects=True)
    client.get('/index', follow_redirects=True)

def test_search(client):
    client.post('/search', follow_redirects=True)

def test_register(client):
    client.post('/register')

def test_user_profile(client):
    client.get('/user_profile')

def test_movie_page(client):
    pass
#    client.get('/movie/<movie_id>')

def test_models(client):
    from app import models
    u = models.User("test", "test@test.com", "test", True)

def test_pdb(client):
    try:
        if os.environ["JAY_TEST"] == "True":
            pytest.set_trace()
    except:
        pass

'''
class spoiled_tomatillos_test_class(unittest.TestCase): 
    # initialization logic for the test suite declared in the test module
    # code that is executed before all tests in one test run
    @classmethod
    def setUpClass(cls):
        pass 

    # clean up logic for the test suite declared in the test module
    # code that is executed after all tests in one test run
    @classmethod
    def tearDownClass(cls):
        pass 

    # initialization logic
    # code that is executed before each test
    def setUp(self):
        pass
#        my_app.app.testing = True
#        self.app = my_app.app.test_client()

    # clean up logic
    # code that is executed after each test
    def tearDown(self):
        pass 

    # test method
    def test_equal_numbers(self):
        self.assertEqual(2, 2) 
        
# runs the unit tests in the module
if __name__ == '__main__':
    unittest.main()
'''
