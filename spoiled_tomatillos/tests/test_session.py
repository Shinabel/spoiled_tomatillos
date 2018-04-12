import os
import unittest
from config import Config
import pytest
from app import app

class SpoiledTestClass(unittest.TestCase):

    def setUp(self):
        self.app = app
        Config.WTF_CSRF_ENABLED = False
        self.app.config.from_object(Config)
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def login(self, username, password):
        return self.client.post('/login', content_type='application/x-www-form-urlencoded', 
                follow_redirects=True,
                data={'username': username, 'password': password})

    def logout(self):
        return self.client.get('/logout')

    def test_login_logout(self):
        self.login('admin', 'admin')
        self.logout()

if __name__ == "__main__":
    unittest.main()

