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

    def add_friends(self):
        self.client.get('/add_friend/3')

    def remove_friend(self):
        self.client.get('/unfriend/3')

    def other_profile(self, pid):
        self.client.get('/user_profile/{}'.format(pid))

    def get_edit_page(self):
        self.client.get('/user_profile/0/edit')

    def test_session(self):
        self.login('admin', 'admin')
        self.add_friends()
        self.get_edit_page()
        self.other_profile(0)
        self.other_profile(3)
        self.other_profile(8)
        self.remove_friend()
        self.remove_friend()
        self.logout()

if __name__ == "__main__":
    unittest.main()

