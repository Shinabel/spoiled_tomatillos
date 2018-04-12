import unittest
import os
from config import Config
import pytest
import random
from app.token import generate_confirmation_token, confirm_token
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

@pytest.fixture
def tester_client():
    from app import app
    Config.WTF_CSRF_ENABLED = False
    app.config.from_object(Config)
    client = app.test_client()
    yield client

'''
@pytest.fixture
def logged_in_user(request, test_user):
    flask_login.login_user(test_user)
    request.addfinalizer(flask_login.logout_user)
'''  
def test_app(client):
    pass

# def test_db_object(client):
#     from app import db

# def test_create_app(client):
#     from app import create_app
#     create_app()

###
# Testing configuration and database / app instantiation
###

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
    ui.__repr__()

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

###
# Testing login 
###

def test_login_manager(client):
    from app import login_manager

def test_admin_login(tester_client):
    tester_client.post('/login', content_type='application/x-www-form-urlencoded',
        follow_redirects=True,
        data={'username': 'admin', 'password': 'admin'})

def test_account_needs_verify(tester_client):
    tester_client.post('/login', content_type='application/x-www-form-urlencoded',
        follow_redirects=True,
        data={'username': 'do_not_finish', 'password': 'blah'})

def test_invalid_user_pass(tester_client):
    tester_client.post('/login', content_type='application/x-www-form-urlencoded',
        follow_redirects=True,
        data={'username': 'holy', 'password': 'moly'})
'''
def test_logout(tester_client):
    tester_client.post('/login', content_type='application/x-www-form-urlencoded',
        follow_redirects=True,
        data={'username': 'admin', 'password': 'admin'})
    tester_client.post('/logout')
'''

###
# Test home page and search features
###

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

###
# Test registration
###

def test_base_register(client):
    client.post('/register')

def test_valid_register_with_confirm_email(tester_client):
    r = random.randint(1, 9999999)
    em = "{}@adfasdf.com".format(r)
    tester_client.post('/register',
            content_type="application/x-www-form-urlencoded",
            data={'username': "testing{}".format(r), 'email': em,
                'password': "asdfbasdf", 'confirm': "asdfbasdf", "accept_tos": "y"})
    tok = generate_confirmation_token(em)
    tester_client.get("/confirm/{}".format(tok))


def test_user_profile(client):
    client.get('/user_profile')

def test_models(client):
    from app import models
    u = models.User("test", "test@test.com", "test", True)

def test_reset_password(client):
    resp = client.get('/reset_password', content_type="application/x-www-form-urlencoded",
            data={'email': "testing123@adfadsf.com"})
    tok = generate_confirmation_token("testing123@adfadsf.com")
    client.post("/reset_password/new/{}".format(tok), content_type="application/x-www-form-urlencoded",
            data={'password': "abcdefg", 'confirm': "abcdefg"})
    client.post("/reset_password/new/{}".format("asdf"), content_type="application/x-www-form-urlencoded",
            data={'password': "abcdefg", 'confirm': "abcdefg"})
    client.post("/reset_password/new/{}".format("tok"), content_type="application/x-www-form-urlencoded",
            data={'password': "abcdefg"})

def test_reset_password_fail_validate(client):
    resp = client.get('/reset_password', content_type="application/x-www-form-urlencoded",
            data={'email': "testing123@adfadsf.com"})
    tok = generate_confirmation_token("testing123@adfadsf.com")
    client.post("/reset_password/new/{}".format(tok), content_type="application/x-www-form-urlencoded",
            data={'password': "12345", 'confirm': "abcdefg"})

def test_confirm_email(client):
    tok = generate_confirmation_token("testing123@adfadsf.com")
    client.get("/confirm/{}".format(tok))

def test_new_confirm_email(client):
    tok2 = generate_confirmation_token("{}@blah.com".format(random.randint(1,9999999)))
    client.get("/confirm/{}".format(tok2))

def test_bad_confirm_email(client):
    client.get("/confirm/{}".format("InRlc3RAdGVzdC5jb20i.DbBixg.8adBzEtfYfbE1I3rUBi05nTEo6s"))

def test_fail_reset_password(client):
    client.get('/reset_password', content_type="application/x-www-form-urlencoded",
            data={'email': "123@ag9s8g.com"})

###
# Test token file
###

def test_tokens(client):
    from app import token
    tok = token.generate_confirmation_token("test@test.com")
    token.confirm_token(tok)

def test_bad_token(client):
    from app import token
    token.confirm_token(True)

###
# Test form file
###
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


def test_edit_profile(tester_client):
    tester_client.post('/login', content_type='application/x-www-form-urlencoded',
        follow_redirects=True,
        data={'username': 'admin', 'password': 'admin'})
    tester_client.post('/edit_profile',
        content_type='application/x-www-form-urlencoded',
        follow_redirects=True,
        data={'username':'admin', 'about_me':'', 'favorite_movies':'', 'submit':'yes'})
    tester_client.post('/logout')