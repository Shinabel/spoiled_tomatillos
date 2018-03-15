import datetime
from passlib.hash import sha256_crypt
from app import app, db

class User:

	def __init__(self, username, email, password):
		self.id = id
		self.username = username
		self.email = email
		self.password = sha256_crypt.encrypt(str(password))
		self.confirmed = confirmed

	def _change_password(self, password):
		self.password = sha256_crypt.encrypt(str(password))

	def is_active(self):
		return True