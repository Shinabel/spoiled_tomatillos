import datetime
from app import app, db

class User:
	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password = password