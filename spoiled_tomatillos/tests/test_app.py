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
    ui = dbobjects.UserInfo()
    ui.is_active()
    ui.get_id()
    ui.is_authenticated()
    ui.is_anonymous()

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

def test_default_search(client):
    client.get('/search')

def test_movie_search(client):
    client.post('/search', follow_redirects=True,
            content_type="application/x-www-form-urlencoded",
            data={'search': 'batman'})

def test_user_search(client):
    client.post('/search', content_type="application/x-www-form-urlencoded",
            data={'search': 'admin'})

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

def test_tokens(client):
    from app import token
    tok = token.generate_confirmation_token("test@test.com")
    token.confirm_token(tok)

def test_bad_token(client):
    from app import token
    token.confirm_token(True)

def test_reset_form_validate(client):
    from app import forms
    rs = forms.ResetForm()
    rs.validate()
    rs.check_email_registered("lok.j@husky.neu.edu")
    rs.check_initial_validation(True)

def test_register_form_validate(client):
    from app import forms
    rs = forms.RegistrationForm()
    rs.validate()
    rs.check_initial_validation(True)
    rs.check_email_registered("lok.j@husky.neu.edu")
    rs.check_username_registered("admin")

def test_pdb(client):
    try:
        if os.environ["JAY_TEST"] == "True":
            pytest.set_trace()
    except:
        pass

