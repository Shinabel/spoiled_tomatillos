from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from app import db, app


# movie titles table as python object
class title_basic(db.Model):
        __tablename__ = 'title.basics'
        __table_args__ = {'extend_existing': True}

        id = db.Column('tconst', db.Unicode, primary_key=True)
        type = db.Column('titleType', db.Unicode)
        title = db.Column('primaryTitle', db.Unicode)
        year = db.Column('startYear', db.Integer)
        genre = db.Column('genres', db.Unicode)

# actors table as python object
class actors(db.Model):
    __tablename__ = 'name'
    __table_args__ = {'extend_existing': True}

    id = db.Column('nconst', db.Unicode, primary_key=True)
    name = db.Column('primaryName', db.Unicode)
    birthYear = db.Column('birthYear', db.Integer)
    deathYear = db.Column('deathYear', db.Integer)
    profession = db.Column('primaryProfession', db.Unicode)
    knownFor = db.Column('knownForTitles', db.Unicode)

# crew table as python object
class crew(db.Model):
        __tablename__ = 'title.crew'
        __table_args__ = {'extend_existing': True}

        movieId = db.Column('tconst', db.Unicode, primary_key=True)
        directors = db.Column('directors', db.Unicode)
        writers = db.Column('writers', db.Unicode)

# crew table as python object
class roles(db.Model):
        __tablename__ = 'title.principals'
        __table_args__ = {'extend_existing': True}

        movieId = db.Column('tconst', db.Unicode, primary_key=True)
        ordering = db.Column('ordering', db.Integer)
        personID = db.Column('nconst', db.Unicode)
        category = db.Column('category', db.Unicode)
        job = db.Column('job', db.Unicode)
        characters = db.Column('characters', db.Unicode)

# crew table as python object
class ratings(db.Model):
        __tablename__ = 'title.ratings'
        __table_args__ = {'extend_existing': True}

        movieId = db.Column('tconst', db.Unicode, primary_key=True)
        numVotes = db.Column('numVotes', db.Integer)

class user_info(db.Model):
        __tablename__ = 'userinformation'
        __table_args__ = {'extend_existing': True}

        username = db.Column('username', db.Unicode, primary_key=True)
        email = db.Column('email', db.Unicode)
        password = db.Column('password', db.Unicode)












