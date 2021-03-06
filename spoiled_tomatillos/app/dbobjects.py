from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db, app
from hashlib import md5

# movie titles table as python object
class TitleBasic(db.Model):
    __tablename__ = 'title.basics'
    __table_args__ = {'extend_existing': True}

    id = db.Column('tconst', db.Unicode, primary_key=True)
    type = db.Column('titleType', db.Unicode)
    title = db.Column('primaryTitle', db.Unicode)
    year = db.Column('startYear', db.Integer)
    genre = db.Column('genres', db.Unicode)


# actors table as python object
class Actors(db.Model):
    __tablename__ = 'name'
    __table_args__ = {'extend_existing': True}

    id = db.Column('nconst', db.Unicode, primary_key=True)
    name = db.Column('primaryName', db.Unicode)
    birthYear = db.Column('birthYear', db.Integer)
    deathYear = db.Column('deathYear', db.Integer)
    profession = db.Column('primaryProfession', db.Unicode)
    knownFor = db.Column('knownForTitles', db.Unicode)


# crew table as python object
class Crew(db.Model):
    __tablename__ = 'title.crew'
    __table_args__ = {'extend_existing': True}

    id = db.Column('ID', db.Integer, primary_key=True)
    movieId = db.Column('tconst', db.Unicode)
    directors = db.Column('directors', db.Unicode)
    writers = db.Column('writers', db.Unicode)


# crew table as python object
class Roles(db.Model):
    __tablename__ = 'title.principals'
    __table_args__ = {'extend_existing': True}

    id = db.Column('ID', db.Integer, primary_key=True)
    movieId = db.Column('tconst', db.Unicode)
    ordering = db.Column('ordering', db.Integer)
    personID = db.Column('nconst', db.Unicode)
    category = db.Column('category', db.Unicode)
    job = db.Column('job', db.Unicode)
    characters = db.Column('characters', db.Unicode)

# class to represent a user from sql
class UserInfo(db.Model, UserMixin):
    __tablename__ = 'user_info'
    __table_args__ = {'extend_existing': True}

    user_ID = db.Column('user_ID', db.Integer, primary_key=True)
    username = db.Column('username', db.Unicode)
    email = db.Column('email', db.Unicode)
    password = db.Column('password', db.Unicode)
    register_date = db.Column('register_date', db.DateTime, nullable=False)
    confirmed = db.Column('confirmed', db.Boolean, nullable=False, default=False)
    confirmed_date = db.Column('confirmed_date', db.DateTime)
    password_token = db.Column('password_token', db.Unicode)
    about_me = db.Column(db.String(255))
    favorite_movies =db.Column(db.String(255))

    def is_active(self):
        return True

    def get_id(self):
        return self.user_ID

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

# Critic ratings as Python object
class Ratings(db.Model):
    __tablename__ = 'title.ratings'
    __table_args__ = {'extend_existing': True}

    movieId = db.Column('tconst', db.Unicode, primary_key=True)
    numVotes = db.Column('numVotes', db.Integer)
    average_rating = db.Column('averageRating', db.Integer)


# class that represents the user ratings from sql
class UserRatings(db.Model):
    __tablename__ = 'user.ratings'
    __table_args__ = {'extend_existing': True}

    rating_ID = db.Column('rating_ID', db.Integer, primary_key=True)
    user_ID = db.Column('user_ID', db.Integer, db.ForeignKey('user_info.user_ID'))
    movieId = db.Column('tconst', db.Unicode, db.ForeignKey('title.basics.tconst'))
    ratings = db.Column('ratings', db.Float)

# class that represents the user.friends table in sql, foreign keys from user ids
class Friends(db.Model):
    __tablename__ = 'user.friends'
    __table_args__ = {'extend_existing': True}

    friendship_ID = db.Column('friendship_ID', db.Integer, primary_key=True)
    friend1_ID = db.Column('friend1_ID', db.Integer, db.ForeignKey('user_info.user_ID'))
    friend2_ID = db.Column('friend2_ID', db.Unicode, db.ForeignKey('user_info.user_ID'))


# class that represents the user.favorites table in sql, foreign keys from user ids, and movie ids
class Favorites(db.Model):
    __tablename__ = 'user.favorites'
    __table_args__ = {'extend_existing': True}

    favorite_ID = db.Column('favorite_ID', db.Integer, primary_key=True)
    user_ID = db.Column('user_ID', db.Integer, db.ForeignKey('user_info.user_ID'))
    movieId = db.Column('tconst', db.Unicode, db.ForeignKey('title.basics.tconst'))
    note = db.Column('note', db.Unicode)
