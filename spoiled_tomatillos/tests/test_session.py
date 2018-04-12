import os
import unittest
from config import Config
import pytest
from app import app
import random


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
        
    def get_user_profile(self):
        self.client.get('/user_profile')

    def get_movie_page(self, mid):
        self.client.get('/movie/{}'.format(mid))

    def get_user_profile(self):
        self.client.get('/user_profile')

    def get_edit_page(self):
        self.client.get('/user_profile/0/edit')

    def get_edit_profile(self):
        self.client.get('/edit_profile')

    def rate_movie(self, mid, rate):
        return self.client.post('/movie/{}'.format(mid), content_type='application/x-www-form-urlencoded', 
                follow_redirects=True,
                data={'user-rating': rate})

    def favorite_movie(self, mid):
        return self.client.post('/movie/{}'.format(mid), content_type='application/x-www-form-urlencoded', 
                follow_redirects=True,
                data={'favorite': 'true'})

    def unfavorite_movie(self, mid):
        return self.client.post('/movie/{}'.format(mid), content_type='application/x-www-form-urlencoded', 
                follow_redirects=True,
                data={'favorite': 'false'})

    def test_session(self):
        self.login('admin', 'admin')
        self.get_user_profile()
        self.add_friends()
        self.get_edit_page()
        #valid form test
        self.get_edit_profile()
        self.other_profile(0)
        self.other_profile(3)
        self.other_profile(8)
        #no genre
        self.get_movie_page('tt0000502')
        #image link available
        self.get_movie_page('tt7783322')

        self.favorite_movie('tt7783322')
        self.unfavorite_movie('tt7783322')
        self.unfavorite_movie('tt7783322')

        self.remove_friend()
        self.remove_friend()
        self.logout()

    def test_session_movie(self):
        self.login('emailtest', 'test')
        #have rated
        self.get_movie_page('tt7783322')
        self.get_movie_page('tt7634968')
        self.rate_movie('tt7634968', 1)
        r = random.randint(1, 9999999)
        self.rate_movie('abel', 1)
        self.rate_movie(r, 1)
        #favorite movie
        self.favorite_movie('tt7783322')
        self.favorite_movie('tt7783322')

        self.favorite_movie('tt0371746')

        self.favorite_movie(r)
        self.favorite_movie(r)

        self.logout()

    def test_session_movie_two(self):
        self.login('ratingTester', 'test')
        self.get_movie_page('tt7783322')

        #favorite movie
        self.favorite_movie('tt7783322')
        self.favorite_movie('tt7783322')


        r = random.randint(1, 9999999)
        self.favorite_movie(r)
        self.favorite_movie(r)
        self.logout()

    def test_session_rate_movie(self):
        #not logged in case
        self.rate_movie('tt7634968', 1)

    def test_friend(self):
        self.login('testing9323379', 'asdfbasdf')
        self.remove_friend()
        self.logout()

if __name__ == "__main__":
    unittest.main()

