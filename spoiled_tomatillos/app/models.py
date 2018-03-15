import datetime
from passlib.hash import sha256_crypt
from app import app, db

class User:
	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password = sha256_crypt.encrypt(str(password))
